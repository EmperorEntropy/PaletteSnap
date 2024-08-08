###
# Modules
###

# External modules
import os
import subprocess
import psutil
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
def loadCache(name : str) -> None:
    '''loads the palette from the file path in the cache dir'''
    cacheDir = setup.cache
    if name == "palette":
        console.log("Illegal name. Please try a different name.")
        raise Exit()
    elif name == "random":
        console.log("Randomly picking a cached palette.")
        # pick a random cached palette
        exclude = ["palette.toml", "PaletteTest.html", "styles.css"]
        allFiles = os.listdir(cacheDir)
        cachedPalettes = [file for file in allFiles if file not in exclude]
        fileName = choice(cachedPalettes)
        filePath = os.path.join(cacheDir, f"{fileName}")
        console.log(f"Cached palette {fileName} chosen.")
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
        imgDict = {"image" : textPalette["image"]}
        palette : dict[str, Color] = {key: hexColor(value) for key, value in textPalette.items() if key != "image"}
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
        exportAll(palette, "cached")

def clearCache(name: str) -> None:
    '''removes file at file path in the cache dir'''
    cacheDir = setup.cache
    exclude = ["palette.toml", "PaletteTest.html", "styles.css"]
    if name == "all":
        for fileName in os.listdir(cacheDir):
            filePath = os.path.join(cacheDir, f"{fileName}")
            if os.path.isfile(filePath) and fileName not in exclude:
                os.remove(filePath)
        console.log("Cache directory has been [green]succesfully[/green] cleared.")
    elif name == "palette":
        console.log("Illegal name. Please try a different name.")
        raise Exit()
    else:
        filePath= os.path.join(cacheDir, f"{name}.toml")
        os.remove(filePath)
        console.log("Cached file has been [green]succesfully[/green] cleared.")

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

def cachePalette(name : str) -> None:
    '''caches the current palette by creating the file palette in the cache dir'''
    console.log(f"Caching current palette to {name}.toml.")
    if name in ["palette", "all", "random"] or '.' in name:
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