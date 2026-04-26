#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Encode URL
# @raycast.mode silent
# @raycast.mode fullOutput - for debugging 
# @raycast.packageName Developer Utilities

# Optional parameters:
# @raycast.icon 💻
# @raycast.argument1 {"type": "dropdown", "placeholder": "Type: default=qs )", "data": [{"title": "<default>qs", "value": "qs"}, { "title": "All - whole url", "value": "whole" }], "optional": true}
# @raycast.argument1 { "type": "text", "placeholder": "whole | -w (optional)", "optional": true }

# Documentation:
# @raycast.description Encodes clipboard URL. Default: only re-encode query string; --whole/-w: encode entire URL.

FLAG="$1"

# Read clipboard (explicit general pasteboard)
CLIP="$(pbpaste -pboard general 2>/dev/null)"

if [ -z "$(printf %s "$CLIP" | tr -d '[:space:]')" ]; then
  echo "Clipboard is empty"
  exit 0
fi

# Avoid piping via stdin (Node stdin can be empty in Raycast script-command context). Instead pass via env.
ENCODED="$(CLIP_INPUT="$CLIP" node - "$FLAG" <<'NODE'
const input = (process.env.CLIP_INPUT || "").trim();
const flagWhole = process.argv.includes("whole");

if (!input) {
  process.stdout.write("");
  process.exit(0);
}

if (flagWhole) {
  process.stdout.write(encodeURIComponent(input));
  process.exit(0);
}

// Preserve hash (#...)
const hashIndex = input.indexOf("#");
const hash = hashIndex >= 0 ? input.slice(hashIndex) : "";
const withoutHash = hashIndex >= 0 ? input.slice(0, hashIndex) : input;

// Split into base and query (?..)
const qIndex = withoutHash.indexOf("?");
const basePart = qIndex >= 0 ? withoutHash.slice(0, qIndex) : withoutHash;
const queryPart = qIndex >= 0 ? withoutHash.slice(qIndex + 1) : "";

// Parse and re-encode query params only
const params = new URLSearchParams(queryPart);
const pairs = [];
for (const [k, v] of params) {
  // Note: this will encode values as-is (may double-encode if already encoded)
  if (v === "") {
    const hadEquals = queryPart.split("&").some(p => p.startsWith(k + "="));
    pairs.push(hadEquals ? `${encodeURIComponent(k)}=${encodeURIComponent(v)}` : encodeURIComponent(k));
  } else {
    pairs.push(`${encodeURIComponent(k)}=${encodeURIComponent(v)}`);
  }
}

let out = basePart;
if (pairs.length) out += `?${pairs.join("&")}`;
else if (qIndex >= 0 && queryPart === "") out += "?";
out += hash;

process.stdout.write(out);
NODE
)"

printf %s "$ENCODED" | pbcopy -pboard general

echo "Encoded URL (copied to clipboard)"
