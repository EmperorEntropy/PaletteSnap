###
# Modules
###

# External modules
import os
import toml
from string import Template

# Internal modules
from . import setup
from .refresh import refreshProgram
from .console import console
from .colorClass import Color

###
# PaletteSnap built-in export functions
###
def exportHTML(colorVarietyFlag):
    '''exports HTML template file for viewing'''
    path = os.path.join(setup.cache, "PaletteTest.html")
    htmlTemplate = Template('''
    <!doctype html>
<html>
<head>
<link rel="stylesheet" href="styles.css">
<style>
    div {
        white-space: pre-wrap;
        margin: 30px;
        padding: 15px;
    }
</style>
<title>PaletteSnap Test</title>
</head>
<body>
<h1>Test Terminal:</h1>
More color variety: $variety
<div><span id="red">from</span> <span id="yellow">PIL</span> <span id="red">import</span> <span id="green">ImageColor</span>
    
<span id="comment"># Distance function</span>
<span id="red">def</span> <span id="green">distance</span>(p1, p2):
    x1, y1, z1 <span id="orange">=</span> p1
    x2, y2, z2 <span id="orange">=</span>  p2
    <span id="red">return</span> ((x2 <span id="orange">-</span> x1)<span id="orange">**</span><span id="magenta">2</span> <span id="orange">+</span> (y2 <span id="orange">-</span> y1)<span id="orange">**</span><span id="magenta">2</span> <span id="orange">+</span> (z2 <span id="orange">-</span> z1)<span id="orange">**</span><span id="magenta">2</span>)<span id="orange">**</span><span id="magenta">2</span>

<span id="comment"># Color class</span>
<span id="red">class</span> <span id="yellow">Color</span>:
    <span id="red">def</span> <span id="green">__init__</span>(<span id="magenta">self</span>, hex):
        <span id="magenta">self</span>.<span id="blue">hex</span> <span id="orange">=</span> hex
        <span id="magenta">self</span>.<span id="blue">hexDigits</span> <span id="orange">=</span> <span id="magenta">self</span>.<span id="blue">hex</span>[<span id="magenta">1</span>:]
        <span id="magenta">self</span>.<span id="blue">rgb</span> <span id="orange">=</span> ImageColor.<span id="green">getrgb</span>(<span id="magenta">self</span>.<span id="blue">hex</span>)
    
    <span id="red">def</span> <span id="green">__repr__</span>(<span id="magenta">self</span>):
        <span id="red">return</span> <span id="cyan">"Hex string: "</span> <span id="orange">+</span> <span id="magenta">self</span>.<span id="blue">hex</span>
</div>
</body>
</html>              
    ''')
    htmlRes = htmlTemplate.substitute(
        variety = str(colorVarietyFlag)
    )
    # Overwrite file at path
    output = open(path, "w")
    output.write(htmlRes)
    output.close()


def exportCSS(colorDict : dict[str, Color]) -> None:
    '''exports palette as CSS file'''
    path = os.path.join(setup.cache, "styles.css")
    cssTemplate = Template('''
    div {
        color: $fg;
        background-color: $bg0;
        border: 3px solid $fg;
    }
    ::-moz-selection { /* Code for Firefox */
    background: $selection;
    }
    ::selection {
    background: $selection;
    }
    #comment {
        color: $comment !important;
    }
    #red {
        color: $red !important; 
    }
    #green {
        color: $green !important;
    }
    #orange {
        color: $orange !important;
    }
    #magenta {
        color: $magenta !important;
    }
    #yellow {
        color: $yellow !important;
    }
    #blue {
        color: $blue !important;
    }
    #cyan {
        color: $cyan !important;
    }              
    ''')
    # comment and selection color dependent on mode
    # if paletteMode == "light":
    #     commentColor = colorDict["bg2"]
    #     selectionColor = colorDict["bg5"]
    # else:
    #     commentColor = colorDict["bg3"]
    #     selectionColor = colorDict["bg4"]
    commentColor = colorDict["bg3"].hex
    selectionColor = colorDict["bg4"].hex

    cssRes = cssTemplate.substitute(
        fg = colorDict["fg"].hex,
        bg0 = colorDict["bg0"].hex,
        comment = commentColor,
        selection = selectionColor,
        red = colorDict["red"].hex,
        green = colorDict["green"].hex,
        orange = colorDict["orange"].hex,
        magenta = colorDict["magenta"].hex,
        yellow = colorDict["yellow"].hex,
        blue = colorDict["blue"].hex,
        cyan = colorDict["cyan"].hex
    )
    # Overwrite file at path
    output = open(path, "w")
    output.write(cssRes)
    output.close()

###
# Template export functions
###
def replaceVar(tempContents : str, palette : dict[str, Color]) -> str:
    '''replaces variable in template with colors in palette'''
    # replace vars with colors
    for key in palette:
        if key == "image":
            # image
            tempContents = tempContents.replace("{{" + key + "}}", palette[key])
        else:
            # hex
            tempContents = tempContents.replace("{{" + key + "}}", palette[key].hex)
            tempContents = tempContents.replace("{{" + key + ".digits}}", (palette[key].hex)[1:])
            # rgb
            tempContents = tempContents.replace("{{" + key + ".r}}", str(palette[key].rgb[0]))
            tempContents = tempContents.replace("{{" + key + ".g}}", str(palette[key].rgb[1]))
            tempContents = tempContents.replace("{{" + key + ".b}}", str(palette[key].rgb[2]))
            # normalized rgb
            tempContents = tempContents.replace("{{" + key + ".nr}}", str(palette[key].normalRgb[0]))
            tempContents = tempContents.replace("{{" + key + ".ng}}", str(palette[key].normalRgb[1]))
            tempContents = tempContents.replace("{{" + key + ".nb}}", str(palette[key].normalRgb[2]))
    return tempContents

def exportTemplates(palette : dict[str, Color]) -> None:
    '''export templates'''
    console.log("Generating templates.")
    templateInfo = toml.load(setup.templateFile)
    for program in templateInfo:
        programInfo = templateInfo[program][0] # dictionary
        # extract information
        for key, value in programInfo.items():
            if key == "name":
                name = value
            elif key == "alias":
                alias = value
            elif key == "dir":
                dir = os.path.expanduser(value)
            else:
                cmd = value
        # handle empty information
        if alias == "":
            alias = name
        if dir == "":
            dir = setup.cache
        # replace variables for template
        tempLoc = os.path.join(setup.templateDir, name)
        exportLoc = os.path.join(dir, alias)
        # check if template file exists
        if os.path.isfile(tempLoc):
            file = open(tempLoc, "r")
            template = file.read()
            file.close()
            # generate the file based on the template
            newContents = replaceVar(template, palette)
            with open(exportLoc, "w") as newFile:
                newFile.write(newContents)
            newFile.close()
            console.log(f"Template {name} succesfully generated.")
        else:
            console.log(f"Template {name} does not exist.")
        # refresh the program
        if cmd != "":
            refreshProgram(program, cmd)

###
# Export all
###

def exportAll(colors : dict[str, Color], flag : str) -> None:
    exportHTML(flag)
    exportCSS(colors)
    exportTemplates(colors)