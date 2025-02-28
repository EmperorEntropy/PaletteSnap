###
# Modules
###

# Internal Modules
from . import setup
from .PaletteSnap import extractPalette
from .wallpaper import setWallpaper
from .templating import exportAll
from .console import console
from .preview import previewPalette
from .cache import cacheSet, loadCache, loadRandomCache, removeCache, clearCache, listCache, renameCache, checkAll
from .outdatedCheck import outdatedCheck

# External Modules
import typer
from typing_extensions import Annotated
import time

###
# Functions
###
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
cache_app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, help="Manipulates the cache.")
app.add_typer(cache_app, name="cache")

# gen command
@app.command()
def gen(
    path: Annotated[
        str,
        typer.Argument(help="Path to wallpaper image.")
    ],
    skip: Annotated[
        bool,
        typer.Option(
            help="Skip creating templates and setting wallpaper.", rich_help_panel="Options"
        ),
    ] = False,
    mode : Annotated[
        str,
        typer.Option(
            help="Theme mode. light, dark, or auto.", rich_help_panel="Options"
        ),
    ] = "auto",
    dominant : Annotated[
        int,
        typer.Option(
            help="Number of dominant colors to pick from image for background. Must be >= 2.", rich_help_panel="Options"
        ),
    ] = 5,
    extra: Annotated[
        bool,
        typer.Option(
            help="Toggles extra colors.", rich_help_panel="Variety"
        ),
    ] = False,
    mix: Annotated[
        bool,
        typer.Option(
            help="Toggles extra colors.", rich_help_panel="Variety"
        ),
    ] = False,
    tweak: Annotated[
        bool,
        typer.Option(
            help="Toggles extra colors.", rich_help_panel="Variety"
        ),
    ] = False,
    sample : Annotated[
        int,
        typer.Option(
            help="Number of colors to sample from images to find accent colors.",
            rich_help_panel="Options"
        ),
    ] = 10000,
    mixAmount: Annotated[
        float,
        typer.Option(
            "--mixAmount", "-ma",
            help="Percentage amount accent color should be mixed with picked color. 0 to 1.", rich_help_panel="Mix Settings"
        ),
    ] = 0.1,
    mixThreshold : Annotated[
        float,
        typer.Option(
            "--mixThreshold", "-mt",
            help="Distance threshold for mixing.", rich_help_panel="Mix Settings"
        ),
    ] = 0.16,
    iterations : Annotated[
        int,
        typer.Option(
            "--iterations", "-i",
            help="Number of iterations for optimization to run.",
            rich_help_panel="Options"
        ),
    ] = 10000,
    weight : Annotated[
        int,
        typer.Option(
            help="Uniqueness weight for optimization. Larger means more unique.",
            rich_help_panel="Options"
        ),
    ] = 100,
    cache : Annotated[
        str,
        typer.Option(
            help="Name of palette to be cached as.",
            rich_help_panel="Options"
        ),
    ] = None,
    hueThreshold : Annotated[
        float,
        typer.Option(
            "--hueThreshold", "-ht",
            help="Distance threshold for hue.", rich_help_panel="Tweak Settings"
        ),
    ] = 10.0,
    hueFactor : Annotated[
        float,
        typer.Option(
            "--hueFactor", "-hf",
            help="Factor of defined accent color hue. 0 to 1.", rich_help_panel="Tweak Settings"
        ),
    ] = 1.0,
    chromaThreshold : Annotated[
        float,
        typer.Option(
            "--chromaThreshold", "-ct",
            help="Threshold for chroma.", rich_help_panel="Tweak Settings"
        ),
    ] = 3.0,
    chromaFactor : Annotated[
        float,
        typer.Option(
            "--chromaFactor", "-cf",
            help="Factor of defined accent color chroma. 0 to 1.", rich_help_panel="Tweak Settings"
        ),
    ] = 0.25,
):
    '''
    Generates color palette given path to image and optional arguments.
    '''
    outdatedCheck()
    # precheck
    if mode not in ["auto", "light", "dark"]:
        raise typer.BadParameter(f"{mode} is not a valid mode. Allowed values are auto, light, and dark.")
    if dominant <= 1:
        console.log("Illegal number of dominant colors.")
    if mode == "auto" and dominant != 5:
        console.log("Mode must not be auto for dominant option to be used.")
    # functionality
    if skip:
        start = time.time()
        # Only create palette
        palette = extractPalette(path, mode, dominant, extra, mix, tweak, sample, mixAmount, mixThreshold, iterations, weight, hueThreshold, hueFactor, chromaThreshold, chromaFactor, True)
        # cache
        if cache is not None:
            cacheSet(cache)
        end = time.time()
        console.log(f"Process [green]completed[/green] in {end-start} seconds.")
    else:
        start = time.time()
        # extract palette
        palette = extractPalette(path, mode, dominant, extra, mix, tweak, sample, mixAmount, mixThreshold, iterations, weight, hueThreshold, hueFactor, chromaThreshold, chromaFactor, True)
        # set wallpaper background
        setWallpaper(path)
        # export templates
        exportAll(palette)
        # cache
        if cache is not None:
            cacheSet(cache)
        end = time.time()
        console.log(f"Process [green]completed[/green] in {end-start} seconds.")

# preview command
@app.command()
def preview(
    image : Annotated[
        bool,
        typer.Option(
            help="Flag for image in preview output.",
            rich_help_panel="Customization"
        ),
    ] = True,
):
    '''Previews current color palette.'''
    outdatedCheck()
    previewPalette(image)

###
# cache command
###

@cache_app.command("set")
def cache_set(
    name: Annotated[
        str,
        typer.Argument(help="Name of cached palette to set to.")
    ],
):
    '''Caches the current color palette with the given name.'''
    start = time.time()
    outdatedCheck()
    cacheSet(name)
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("load")
def cache_load(
    name: Annotated[
        str,
        typer.Argument(help="Name of cached palette.")
    ],
):
    '''Loads the cached palette given a name.'''
    start = time.time()
    outdatedCheck()
    loadCache(name)
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("random")
def cache_random():
    '''Loads a random cached palette.'''
    start = time.time()
    outdatedCheck()
    loadRandomCache()
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("remove")
def cache_remove(
    names: Annotated[
        list[str],
        typer.Argument(help="Names of cached palette.")
    ],
):
    '''Removes cached palettes.'''
    start = time.time()
    outdatedCheck()
    removeCache(names)
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("clear")
def cache_clear(
    skip: Annotated[
        bool,
        typer.Option(help="Skips the confirmation prompt.")
    ] = False,
):
    '''Clears all cached palettes.'''
    start = time.time()
    outdatedCheck()
    if not skip:
        prompt = typer.confirm("Are you sure you want to clear the entire cache?")
        if prompt:
            clearCache()
        else:
            console.log()
            raise typer.Exit()
    else:
        clearCache()
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("list")
def cache_list():
    '''Lists all cached palettes.'''
    start = time.time()
    outdatedCheck()
    listCache()
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("rename")
def cache_rename(
    oldName: Annotated[
        str,
        typer.Argument(help="Present name of cached palette.")
    ],
    newName : Annotated[
        str,
        typer.Argument(help="New name for cached palette.")
    ],
):
    '''Renames a cached palette.'''
    start = time.time()
    outdatedCheck()
    renameCache(oldName, newName)
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")

@cache_app.command("check")
def cache_check():
    '''Checks all the cached palettes.'''
    start = time.time()
    outdatedCheck()
    checkAll()
    end = time.time()
    console.log(f"Process [green]completed[/green] in {end-start} seconds.")
