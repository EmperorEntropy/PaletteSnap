<header>
    <br>
    <h2 align="center">PaletteSnap</h2>
    <p align="center">
        Generate readable color palettes from any image!
    </p>
    <p align="center">
    <img alt="Static Badge" src="https://img.shields.io/badge/pip_install-palettesnap-blue?style=flat-square">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/palettesnap?style=flat-square&color=green">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/palettesnap?style=flat-square&label=PaletteSnap&link=https%3A%2F%2Fpypi.org%2Fproject%2Fpalettesnap%2F">
    <img alt="Pepy Total Downlods" src="https://img.shields.io/pepy/dt/palettesnap?style=flat-square&color=red">
    </p>
</header>

**The README file gives you a "snap" of PaletteSnap. Consult the [Wiki](https://github.com/EmperorEntropy/PaletteSnap/wiki) for more detailed information.**

## Installation
PaletteSnap is a python program, so Python is needed. It can be installed via pip:
```
pip install palettesnap
```
It is not recommended to install PaletteSnap via the Github repository due to changes that may or may not break. Wait for new releases, and download them via `pip`.

Note that PaletteSnap depends on many dependencies, and it might take a while for it to execute during its first run.

## Demonstration

https://github.com/user-attachments/assets/5afe9fac-1e76-48cf-af2e-3f04894dfc3a

## Examples
![](https://snipboard.io/06j3rB.jpg)

![](https://snipboard.io/w6vlx3.jpg)

![](https://snipboard.io/tBTeh6.jpg)

## Features
- Generates a color palette from any image.
- Color palette are guaranteed to be readable with good contrast.
- Options to increase color variety for palette. Useful for monochromatic images.
- Assigned color roles. No more guessing which color does want with the palette.
- Sets wallpaper to your image automatically.
- Uses templates so that you can apply the color palette to your entire system.
- Has caching so you can load pre-generated palettes fast.
- Supports program refreshing. No more closing and reopening programs to get them to update their palette.
- Auto checks for updates. Get notified when a new version gets released.

### Comparison
Here is a table that compares PaletteSnap with pywal:
|                               |      **pywal**     |   **PaletteSnap**  |
|:-----------------------------:|:------------------:|:------------------:|
|       **Palette Generation**      | :white_check_mark: | :white_check_mark: |
|     **Wallpaper Setting**     | :white_check_mark: | :white_check_mark: |
|         **Templating**        | :white_check_mark: | :white_check_mark: |
|      **Readable Palette**     |      :warning:     | :white_check_mark: |
|      **Preview Palette**     |      :white_check_mark:    | :white_check_mark: |
| **Assigned Color Roles** |         :x:        | :white_check_mark: |
| **Color Variety Options** |         :x:        | :white_check_mark: |
|     **Refreshes Programs**    |         :x:        | :white_check_mark: |
|  **Custom Background Color**  | :white_check_mark: |         :warning:        |
|    **Cached colorschemes**    | :white_check_mark: | :white_check_mark: |
|    **Color palette modes**    |  :warning: |     :white_check_mark:     |
|     **Random palette**        | :white_check_mark: | :white_check_mark: |
|     **Update Checker**    |         :x:        | :white_check_mark: |

### Wallpaper Setting
PaletteSnap's functionality is supported by all OS that has Python. However, the wallpaper switching functionality may not be supported for certain OS. Here is a list of all OS that PaletteSnap's wallpaper switching supports:
- macOS (tested)
- GNOME Linux (untested)
- KDE Plasma Linux (tested)
- XFCE Linux (untested)
- MATE Linux (untested)

If you have one of the untested OS, and it works, please let me know. If you have an OS that is not on the list, feel free to suggest it!

## Usage
When generating the palette, PaletteSnap creates two folders. They are
- `XDG_CONFIG_HOME/palsnap`
- `XDG_CACHE_HOME/palsnap`

On a macOS, they are `~/.config/palsnap/` and `~/.cache/palsnap/`. The folders palsnap can be found in are the same folders pywal's config and cache are found in.

*For the sake of convenience, the locations of these folders will be referred to as macOs's in the rest of the README file.*

### Palette Generation
To generate a palette, run the following command:
`palsnap gen <img_path>`
This is the simplest way to generate a palette. If you run `palsnap gen -h`, you'll notice there is a list of options.

If you keep hitting the *manual optimization* for your generated palette, this is usually a sign that your current options are not good. If you haven't already, an easy way to avoid it is to set your `mode` to either light or dark instead of auto.

**See [Palette Generation](https://github.com/EmperorEntropy/PaletteSnap/wiki/Palette-Generation) for further information.**

### Preview
In order to preview a palette, you must first generate it. You can skip all the other steps in the process by running `palsnap gen <img_path> --skip`. After that, run `palsnap preview` to preview the palette. The output will be the image (only for certain terminals) and all the colors. Your terminal window must be big enough to see all the colors. 

If you want a more direct approach, in the `~/.cache/palsnap` folder, there should be a `PaletteTest.html`. You can use it to see what your palette will actually look like if you use it.

**See [Previewing](https://github.com/EmperorEntropy/PaletteSnap/wiki/Previewing) for further information.**

### Templating
All templating information is done in `~/.config/palsnap/templates.toml` and templates are stored in the templates folder found at `~/.config/palsnap/templates/`.

**See [Templating](https://github.com/EmperorEntropy/PaletteSnap/wiki/Templating) for further information.**

### Caching
To save time, it is possible to cache palettes. You can either cache palettes as you generate them with the `--cache` option, or you can cache the palette right after generating it with:
```
palsnap cache set <name>
```
The latter method is useful if you want to generate and preview the palette before caching it. There are many other cache commands like `load`, `clear`, `rename`, etc.

**See [Caching](https://github.com/EmperorEntropy/PaletteSnap/wiki/Caching) for further information.**

### Color Palette
Based on Everforest's palette usage,
| Identifier | Usages |
|---|---|
| `bg` | Default Background |
| `bg1` | Unused |
| `bg2` | Unused |
| `bg3` | Comment color |
| `bg4` | Selection background color |
| `bg5` | Unused |
| `foreground` | Default Foreground, [_Treesitter_: Constants, Variables, Function Parameters, Properties, Symbol Identifiers] |
| `red` | Conditional Keywords, Loop Keywords, Exception Keywords, Inclusion Keywords, Uncategorised Keywords, Diff Deleted Signs, Error Messages, Error Signs |
| `orange` | Operator Keywords, Operators, Labels, Storage Classes, Composite Types, Enumerated Types, Tags, Title, Debugging Statements |
| `yellow` | Types, Special Characters, Warning Messages, Warning Signs, [_Treesitter_: Modules, Namespaces] |
| `green` | Function Names, Method Names, Strings, Characters, Hint Messages, Hint Signs, Search Highlights, [_Treesitter_: Constructors, Function Calls, Built-In Functions, Macro Functions, String Escapes, Regex Literals, Tag Delimiters, Non-Structured Text] |
| `cyan` | Constants, Macros, [_Treesitter_: Strings, Characters] |
| `blue` | Identifiers, Uncategorised Special Symbols, Diff Changed Text Background, Info Messages, Info Signs, [_Treesitter_: Fields, Special Punctuation, Math Environments] |
| `magenta` | Booleans, Numbers, Preprocessors, [_Treesitter_: Built-In Constants, Built-In Variables, Macro-Defined Constants, Attributes/Annotations] |
| `violet` | Unused. Can be used to replace `magenta` if wanted. |
| `white` | ANSI white |
| `black` | ANSI black |

`cusor_bg` is usually just the foreground. `cursor_fg` is usually just the background.

**See [Color Roles](https://github.com/EmperorEntropy/PaletteSnap/wiki/Color-Roles) for further information.**

## To Do
- Add option for users to define number of bg gradients.
- Add more flexibility to determine bg.
- Add check for templating that returns list of variables not replaced.
- Add wallpaper setting support for more Linux distributions.
- Add image preview support for more terminals.

## Acknowledgments
- [pywal](https://github.com/dylanaraps/pywal) for the inspiration that led me to create PaletteSnap.
- Contributors in pull requests for adding or fixing features.
- [ozwaldorf](https://github.com/ozwaldorf/) for helpful suggestions and advice during PaletteSnap's initial development. Check out [lutgen](https://github.com/ozwaldorf/lutgen-rs), a program that themes any image to a desktop colorscheme.
- [Everforest colorscheme](https://github.com/sainnhe/everforest/) for its colorscheme usage.
- [Solarized](https://github.com/altercation/solarized) and [Selenized](https://github.com/jan-warchol/selenized) colorschemes for giving me valuable insights on what a palette should be like.
