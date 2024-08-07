###
# Modules
###

# Internal Modules
from .PaletteSnap import extractPalette
from .wallpaper import setWallpaper
from .templating import exportAll
from .console import console
from .preview import previewPalette

# External Modules
import typer
from typing_extensions import Annotated
import time

###
# Functions
###

'''
PaletteSnap has multiple commands:
- gen: generates colorscheme from image
- preview: preview colors of current colorscheme
'''

app = typer.Typer()

@app.command()
def gen(
    path: Annotated[
        str,
        typer.Argument(help="Path to wallpaper image")
    ],
    skip: Annotated[
        bool,
        typer.Option(
            help="Skip creating templates and setting wallpaper", rich_help_panel="Customization"
        ),
    ] = False,
    mode : Annotated[
        str,
        typer.Option(
            help="Theme mode. light, dark, or auto", rich_help_panel="Customization"
        ),
    ] = "auto",
    variety: Annotated[
        str,
        typer.Option(
            help="default, extra, or mix", rich_help_panel="Customization"
        ),
    ] = "default",
    sample : Annotated[
        int,
        typer.Option(
            help="Number of colors to sample from images to find accent colors",
            rich_help_panel="Customization"
        ),
    ] = 10000,
    mixAmount: Annotated[
        float,
        typer.Option(
            "--mixAmount", "-ma",
            help="Percentage amount accent color should be mixed with picked color. 0 to 1", rich_help_panel="Customization"
        ),
    ] = 0.1,
    mixThreshold : Annotated[
        float,
        typer.Option(
            "--mixThreshold", "-mt",
            help="Distance threshold for mixing", rich_help_panel="Customization"
        ),
    ] = 0.16,
    weight : Annotated[
        int,
        typer.Option(
            help="Uniqueness weight for optimization. Larger means more unique",
            rich_help_panel="Customization"
        ),
    ] = 100,
):
    '''
    Generates colorscheme given path to image and optional arguments.
    '''
    # precheck
    if mode not in ["auto", "light", "dark"]:
        raise typer.BadParameter(f"{mode} is not a valid mode. Allowed values are auto, light, and dark.")
    if variety not in ["default", "extra", "mix"]:
        raise typer.BadParameter(f"{variety} is not a valid color variety type. Allowed values are default, extra, and mix.")
    # functionality
    if skip:
        start = time.time()
        # Only create palette
        extractPalette(path, mode, variety, sample, mixAmount, mixThreshold, weight, True)
        end = time.time()
        console.log(f"Process [green]completed[/green] in {end-start} seconds.")
    else:
        start = time.time()
        # extract palette
        palette = extractPalette(path, mode, variety, sample, mixAmount, mixThreshold, weight, True)
        # set wallpaper background
        setWallpaper(path) # setting background
        # export templates
        exportAll(palette, variety)
        end = time.time()
        console.log(f"Process [green]completed[/green] in {end-start} seconds.")


@app.command()
def preview():
    '''Previews current colorscheme.'''
    console.log("Previewing only works if you used a template to change your terminal colors.")
    previewPalette()