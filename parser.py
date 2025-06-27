#!/usr/bin/env python3

### Website parser Proof of concept
# Takes in a text document, parses input, put it out into useable HTML
import re, sys

## Takes in a line and formatCode, formatcode is meant for HTML formatting purposes
def formatter(line, formatCode):
    if formatCode == "a":
        return f'\t<a href="{line}">{line}</a>'
    elif formatCode == "m":
        return f"\t<img src={line}></img>"
    else:
        return f"\t<{formatCode}>{line}</{formatCode}>"

## Cleans Up HTML, arrows and things were actually rendering on the site
def cleanHtml(line):
    return (line
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;"))

## Parses The lines and matches them to case
def parser(line):
    if re.search(r"^#\s", line):          # "#" (Header 1)
        writeOut(formatter(line[2:], "h1"))
    if re.search(r"^##\s", line):         # "##" (Header 2)
        writeOut(formatter(line[3:], "h2"))
    # Things that are text elements
    if re.search(r"^/p\s", line):         # "/p" (paragraph)
        writeOut(formatter(line[3:], "p"))
    if re.search(r"^/b\s", line):         # /b (BOLD)
        writeOut(formatter(line[3:], "b"))
    if re.search(r"^/i\s", line):         # /i (Italics)
        writeOut(formatter(line[3:], "i"))
    if re.search(r"^/s\s", line):         # /s (small)
        writeOut(formatter(line[3:], "small"))
    if re.search(r"^/a\s", line):         # /a (link)
        writeOut(formatter(line[3:], "a"))
    if re.search(r"^/m\s", line):         # /m (image)
        writeOut(formatter(line[3:], "m"))
    if re.search(r"^/t\s", line):         # /t (Custom title thingy)
        writeOut(
f"""<h1>{line[3:]} 
    <span class="cursor">_</span>  
</h1>""")
    if re.search(r"^/u\s", line):         # /u (unordered list)
        writeOut(formatter(line[3:], "ul"))
    if re.search(r"^/l\s", line):         # /l (ordered list)
        writeOut(formatter(line[3:], "li"))
    if re.search(r"^/bk\s", line):        # /bk _ 100 (custom dash seperated line breaks, takes in amount from space left of call)
        writeOut(f"\t<p>{line[4] * int(line[6:])}</p>")
    if re.search(r"^/cs\b", line):         # /cs (code block Start)
        writeOut('<div class="codeBlock"><pre>')     
    if re.search(r"^/c\s", line):         # /c (code block)
        clean = cleanHtml(line[3:])
        writeOut(f"{clean}")    
    if re.search(r"^/ce\b", line):         # /ce (code block End)
        writeOut("</pre></div>")



## Writes output to file
# takes in sysarg 1, formats it as a html file, and then writes it out, should probably change from a to x for file write
def writeOut(input):
    with open(f"{sys.argv[1]}.html", "a") as out:
        out.write(input + "\n")

## Main
# Messy mess of messing, takes in sysarg 1 as input for file
with open(sys.argv[1]) as ingest:
    writeOut(f'<html>')
    writeOut(f'<head>')
    writeOut(f'<link rel="stylesheet" href="/styles.css">')
    writeOut(f'</head>')
    writeOut(f'<body>')
    for line in ingest:
        line = line.strip()
        print(line)
        parser(line)
    writeOut('</body>')
    writeOut("""<footer>
    <p>---------</p>
    <a href="../blog.html">Back</a>
    <a href="/index.html">Home</a>
</footer>""")
    writeOut(f'</html>')
