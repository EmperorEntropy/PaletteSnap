###
# Modules
###

# External modules
import os
import toml
from typer import confirm, Exit
from random import choice

# Internal modules
from . import setup
from .console import console
from .colorClass import Color, hexColor
from .preview import readPalette
from .wallpaper import setWallpaper
from .templating import exportAll

###
# Cache functions
###
def cacheSet(name : str) -> None:
    '''caches the current palette by creating the file palette in the cache dir'''
    console.log(f"Caching current palette to {name}.toml.")
    if name in ["palette"] or '.' in name:
        console.log("Illegal name. Please try a different name.")
        raise Exit()
    else:
        # check if name already exists
        filePath= os.path.join(setup.cache, f"{name}.toml")
        if os.path.exists(filePath):
            console.log(f"Palette with name {name} already exists in cached directory.")
            overwrite = confirm("Do you want to overwrite it?")
            if overwrite:
                palette = readPalette()
                with open(filePath, "w") as file:
                    toml.dump(palette, file)
                file.close()
                console.log("Cache operation [green]completed[/green].")
            else:
                console.log("Cache operation [red]canceled[/red].")
                raise Exit()
        else:
            palette = readPalette()
            with open(filePath, "w") as file:
                toml.dump(palette, file)
            file.close()
            console.log("Cache operation [green]completed[/green].")

def loadCache(name : str) -> None:
    '''loads the palette from the file path in the cache dir'''
    cacheDir = setup.cache
    if name == "palette":
        console.log("Illegal name. Please try a different name.")
        raise Exit()
    else:
        console.log(f"Loading cached {name}.toml.")
        filePath = os.path.join(cacheDir, f"{name}.toml")
    # check if palette exists
    if not os.path.exists(filePath):
        console.log(f"No palette with name {name} exists in cache.")
        console.log("[red]Failed[/red] to load cached palette.")
        raise Exit()
    else:
        # get the palette
        textPalette : dict[str, str] = toml.load(filePath)
        imgDict = {"image" : textPalette["image"], "mode" : textPalette["mode"]}
        palette : dict[str, Color] = {key: hexColor(value) for key, value in textPalette.items() if key != "image" and key != "mode"}
        palette = imgDict | palette
        console.log("Cached file [green]succesfully[/green] loaded.")
        # overwrite palette.toml for previewing
        currPalette = os.path.join(setup.cache, "palette.toml")
        with open(currPalette, "w") as file:
            toml.dump(textPalette, file)
        file.close()
        # set wallpaper background
        imgPath = palette["image"]
        setWallpaper(imgPath)
        # export templates
        exportAll(palette)

def loadRandomCache():
    '''loads a random cached palette'''
    cacheDir = setup.cache
    console.log("Randomly picking a cached palette.")
    # pick a random cached palette
    exclude = ["palette.toml", "PaletteTest.html", "styles.css"]
    allFiles = os.listdir(cacheDir)
    cachedPalettes = [file for file in allFiles if file not in exclude]
    fileName = choice(cachedPalettes)
    console.log(f"Cached palette {fileName} chosen.")
    # load it
    name = os.path.splitext(fileName)[0]
    loadCache(name)


def removeCache(names : list[str]) -> None:
    '''removes cache palettes'''
    cacheDir = setup.cache
    if "palette" in names:
        console.log("palette is an illegal name. It cannot be removed.")
    else:
        for name in names:
            filePath= os.path.join(cacheDir, f"{name}.toml")
            os.remove(filePath)
            console.log(f"Cached file {name} has been [green]succesfully[/green] cleared.")

def clearCache() -> None:
    '''clears the cache'''
    cacheDir = setup.cache
    exclude = ["palette.toml", "PaletteTest.html", "styles.css"]
    for fileName in os.listdir(cacheDir):
        filePath = os.path.join(cacheDir, f"{fileName}")
        if os.path.isfile(filePath) and fileName not in exclude:
            os.remove(filePath)
    console.log("Cache directory has been [green]succesfully[/green] cleared.")

def listCache() -> None:
    '''counts and lists the cached palettes'''
    cacheDir = setup.cache
    exclude = ["palette.toml", "PaletteTest.html", "styles.css"]
    allFiles = os.listdir(cacheDir)
    cachedPalettes = [file for file in allFiles if file not in exclude]
    console.log(f"There are {len(cachedPalettes)} cached palettes:")
    for file in cachedPalettes:
        console.log(f"{file}")
    return None

def renameCache(oldName : str, newName : str) -> None:
    '''renames cached palette'''
    cacheDir = setup.cache
    if oldName == "palette" or newName == "palette" or '.' in oldName or '.' in newName:
        console.log("Illegal name. Please use different name.")
        raise Exit()
    else:
        oldPath = os.path.join(cacheDir, f"{oldName}.toml")
        newPath = os.path.join(cacheDir, f"{newName}.toml")
        os.rename(oldPath, newPath)
        console.log(f"Renamed {oldName}.toml to {newName}.toml.")
    
def checkCache(name : str) -> bool:
    '''checks a cached palette and makes sure it is legal'''
    currPalette = list(readPalette().keys())
    palettePath = os.path.join(setup.cache, f"{name}")
    cachedPalette = list(toml.load(palettePath).keys())
    if currPalette == cachedPalette:
        return True
    else:
        return False

def checkAll() -> None:
    '''checks all cached palettes and returns list of illegal ones'''
    # Get all cached palettes
    cacheDir = setup.cache
    exclude = ["palette.toml", "PaletteTest.html", "styles.css"]
    allFiles = os.listdir(cacheDir)
    cachedPalettes = [file for file in allFiles if file not in exclude]
    illegalPalettes = [palette for palette in cachedPalettes if not checkCache(palette)]
    count = len(illegalPalettes)
    if len(illegalPalettes) == 0:
        console.log("All palettes are well-defined.")
    else:
        console.log(f"[red]{count}[/red] palettes with invaild palette variable names found.")
        console.log(f"{illegalPalettes}")
    
