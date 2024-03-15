#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Escape String (Json)
# @raycast.mode silent 
# @raycast.packageName Transform

# Optional parameters:
# @raycast.icon images/genpasswd.png
# @raycast.iconDark images/genpasswd-iconDark.png

# Documentation:
# @raycast.description Escape string (Json, newline)
# @raycast.author Bright  
# @raycast.authorURL 

import subprocess

# sample code: https://github.com/raycast/script-commands/blob/master/commands/developer-utils/sentry/sentry-unresolved-issues.template.py

# get from clipboard 

currentText = subprocess.run("pbpaste", universal_newlines=True, stdout=subprocess.PIPE).stdout
print("Current text")
print(currentText)

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|pbcopy'
    return subprocess.check_call(cmd, shell=True)

if currentText:
    escapedString = currentText.encode('unicode_escape')
    escapedString = repr(escapedString)[2:-1].replace("\\\\", "\\")
    # unescapedString = currentText.encode('utf-8').decode('unicode_escape')
    # copy2clip(unescapedString)
    # print(unescapedString)
    print(escapedString)
    subprocess.run("pbcopy", universal_newlines=True, input='{}'.format(escapedString))
    # subprocess.run("pbcopy", universal_newlines=True, input='copy')
    # print("Copied to clipboard ")
else:
    print("No input found")
    exit(1)

    # Test with below
    # {
    #     "glossary": {
    #         "title": "example glossary",
    #         "GlossDiv": {
    #             "title": "S",
    #             "GlossList": {
    #                 "GlossEntry": {
    #                     "ID": "SGML",
    #                     "SortAs": "SGML",
    #                     "GlossTerm": "Standard Generalized Markup Language",
    #                     "Acronym": "SGML",
    #                     "Abbrev": "ISO 8879:1986",
    #                     "GlossDef": {
    #                         "para": "A meta-markup language, used to create markup languages such as DocBook.",
    #                         "GlossSeeAlso": ["GML", "XML"]
    #                     },
    #                     "GlossSee": "markup"
    #                 }
    #             }
    #         }
    #     }
