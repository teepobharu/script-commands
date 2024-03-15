#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Unescape String (Json)
# @raycast.mode silent
# @raycast.packageName Transform

# Optional parameters:
# @raycast.icon images/genpasswd.png
# @raycast.iconDark images/genpasswd-iconDark.png

# Documentation:
# @raycast.description Unescape string (Json)
# @raycast.author Bright  
# @raycast.authorURL 

import subprocess

# sample code: https://github.com/raycast/script-commands/blob/master/commands/developer-utils/sentry/sentry-unresolved-issues.template.py

# get from clipboard 

currentText = subprocess.run("pbpaste", universal_newlines=True, stdout=subprocess.PIPE).stdout
print("Current text")
print(currentText)
if currentText:
    unescapedString = currentText.encode('utf-8').decode('unicode_escape')
    subprocess.run("pbcopy", universal_newlines=True, input=unescapedString)

    # subprocess.run("pbcopy", universal_newlines=True, input='copy')
    print("Copied to clipboard")
else:
    print("No input found")
    exit(1)

