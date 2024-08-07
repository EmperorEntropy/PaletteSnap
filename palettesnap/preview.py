###
# Modules
###

# External modules
import os
import subprocess
import psutil
import toml

# Internal modules
from . import setup
from .console import console
from .colorClass import hexToRgb
#import setup
#from console import console
#from colorClass import hexToRgb

###
# Terminal function
###
def getTerminal() -> str:
    '''identify the terminal type'''
    # python script's ppid is terminal shell's pid
    # terminal type is shell's ppid
    # Get the shell's PPID
    shellPID = os.getppid()
    terminalPID = psutil.Process(shellPID).ppid()
    # Get the terminal type
    cmd = f"ps -p {terminalPID} | awk 'NR==2 {{print $NF}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
    result = result[:-1]
    # parse the result
    if "wezterm" in result or "WezTerm" in result:
        return "wezterm"
    else:
        return "NA"

###
# Image function
###

def showImage(path : str, terminal) -> None:
    '''prints the image in the terminal'''
    if terminal == "wezterm":
        subprocess.run(["wezterm", "imgcat", path, "--height", "45%"])
    else:
        console.log("Terminal type not supported for displaying images.")
        console.log("Skipping set to display the image.")

###
# Color function
###
def readPalette() -> dict[str, str]:
    '''reads palette.toml and returns'''
    path = os.path.join(setup.cache, "palette.toml")
    return toml.load(path)

def rgbToAnsi(fg : tuple[int, int, int], bg : tuple[int, int, int], text : str) -> str:
    '''returns text with fg and bg color'''
    fgRed, fgGreen, fgBlue = fg
    bgRed, bgGreen, bgBlue = bg
    res = f"\033[38;2;{fgRed};{fgGreen};{fgBlue}m\033[48;2;{bgRed};{bgGreen};{bgBlue}m"
    res = res + text + "\033[0m"
    return res

def colorRow(label : str, hexColor : str, colorDict : dict[str, str]) -> str:
    '''creates a row for the colors'''
    maxLen = max([len(key) for key in colorDict])
    text = "PaletteSnap"[:maxLen]
    row = label + " " * (maxLen - len(label)) + "|"
    fgColor = hexToRgb(hexColor)
    for key in colorDict:
        bgColor = hexToRgb(colorDict[key])
        row = row + rgbToAnsi(fgColor, bgColor, text) + "|"
    row = row[:-1] + "\n"
    return row

def printColors(colorDict : dict[str, str]) -> None:
    '''prints the colors in the terminal'''
    maxLen = max([len(key) for key in colorDict])
    # first row
    firstRow = " " * maxLen + "|"
    for key in colorDict:
        firstRow = firstRow + key + " " * (maxLen - len(key)) + "|"
    firstRow = firstRow[:-1] + "\n" # remove last |
    finalRes = firstRow
    # do other rows
    for key in colorDict:
        row = colorRow(key, colorDict[key], colorDict)
        finalRes += row
    print(finalRes)
    return None

###
# Main function
###
def previewPalette() -> None:
    # Get image path and colors
    console.log("Terminal must support [blue]24-bit / true color[/blue] for previewing to work.")
    palette = readPalette()
    imgPath = palette["image"]
    palette.pop("image")
    # Get terminal type and print image
    terminal = getTerminal()
    showImage(imgPath, terminal)
    # Print colors
    printColors(palette)