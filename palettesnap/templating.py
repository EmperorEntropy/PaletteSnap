###
# Modules
###

# External modules
import os
import toml
from string import Template
from re import sub, findall

# Internal modules
from . import setup
from .refresh import refreshProgram
from .console import console
from .colorClass import Color

###
# PaletteSnap built-in export functions
###
def exportHTML():
    '''exports HTML template file for viewing'''
    path = os.path.join(setup.cache, "PaletteTest.html")
    htmlRes = '''
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
    '''
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
        background-color: $bg;
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
    # comment and selection color
    commentColor = colorDict["bg3"].hex
    selectionColor = colorDict["bg4"].hex

    cssRes = cssTemplate.substitute(
        fg = colorDict["fg"].hex,
        bg = colorDict["bg"].hex,
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
    modePattern = r"\{\{mode \| (.*?) \| (.*?)\}\}"
    for key in palette:
        if key == "image" or key == "mode":
            # image/mode
            tempContents = tempContents.replace("{{" + key + "}}", palette[key])
            # special case for image
            tempContents = tempContents.replace("{{image.name}}", os.path.basename(palette[key]))
            # special case for mode
            mode = palette["mode"]
            tempContents = sub(modePattern, lambda match: match.group(1) if mode == 'light' else match.group(2), tempContents)
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
            # hsl
            tempContents = tempContents.replace("{{" + key + ".h}}", str(palette[key].hsl[0]))
            tempContents = tempContents.replace("{{" + key + ".s}}", str(palette[key].hsl[1]))
            tempContents = tempContents.replace("{{" + key + ".l}}", str(palette[key].hsl[2]))
    # lighten, darken, and mode inverse
    lightenPattern = r"\{\{(.*?).lighten\(([0-9.\d]+)\)\}\}"
    darkenPattern = r"\{\{(.*?).darken\(([0-9.\d]+)\)\}\}"
    modeInversePattern = r"\{\{(.*?).modeInverse\(([0-9.\d]+)\)\}\}"
    lightenMatches = findall(lightenPattern, tempContents)
    darkenMatches = findall(darkenPattern, tempContents)
    modeInverseMatches = findall(modeInversePattern, tempContents)
    for match in lightenMatches:
        name = match[0]
        value = float(match[1])
        if name in palette:
            currColor = palette[name]
            tempContents = tempContents.replace("{{" + name + ".lighten(" + str(value) + ")}}", Color.lighten(currColor, value).hex)
        else:
            console.log(f"Cannot lighten {name} with value {value}")
    for match in darkenMatches:
        name = match[0]
        value = float(match[1])
        if name in palette:
            currColor = palette[name]
            tempContents = tempContents.replace("{{" + name + ".darken(" + str(value) + ")}}", Color.darken(currColor, value).hex)
        else:
            console.log(f"Cannot darken {name} with value {value}")
    for match in modeInverseMatches:
        mode = palette["mode"]
        name = match[0]
        value = float(match[1])
        # mode inverse darkens a color if the mode is light
        # mode inverse lightens a color if the mode is dark
        if name in palette:
            currColor = palette[name]
            if mode == "light":
                newColor = Color.darken(currColor, value).hex
            else:
                newColor = Color.lighten(currColor, value).hex
            tempContents = tempContents.replace("{{" + name + ".modeInverse(" + str(value) + ")}}", newColor)
        else:
            console.log(f"Cannot apply mode inverse to {name} with value {value}")
    return tempContents

def exportTemplates(palette : dict[str, Color]) -> None:
    '''export templates'''
    console.log("Generating templates.")
    templateInfo = toml.load(setup.templateFile)
    for program in templateInfo:
        programInfo : list[dict[str, str]] = templateInfo[program]
        for tempDict in programInfo:
            # extract information
            for key, value in tempDict.items():
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

def exportAll(colors : dict[str, Color]) -> None:
    exportHTML()
    #exportCSS(colors)
    exportTemplates(colors)