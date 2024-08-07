<header>
    <br>
    <h2 align="center">PaletteSnap</h2>
    <p align="center">
        Generate readable color palettes from any image!
    </p>
</header>

**At the time of writing, PaletteSnap is in early Alpha. Many things are expected to be changed, and it is likely that new features will be added. Feel free to make suggestions.**

---

# Examples
`palsnap gen image.jpg`
![](https://snipboard.io/1qmeQW.jpg)

`palsnap gen image.jpg --variety mix`
![](https://snipboard.io/Ip5cmw.jpg)

`palsnap gen image.jpg --variety mix`
![](https://snipboard.io/Bz312i.jpg)

`palsnap gen image.jpg --mode light --variety mix -mt 0.14`
![](https://snipboard.io/v0yMEf.jpg)

`palsnap gen image.jpg --mode light --sample 100 --variety mix`
![](https://snipboard.io/GisUZQ.jpg)

# Installation
PaletteSnap is a python program, so Python is needed. It can be installed via pip:
`pip install palettesnap`
Note that PaletteSnap depends on many dependencies, and it takes a long time to install and import them. It roughly takes at least 25 seconds for PaletteSnap to import all the packages for its first run.

PaletteSnap's functionality is supported by all OS that has Python. However, the wallpaper switching functionality may not be supported for certain OS. Here is a list of all OS that PaletteSnap's wallpaper switching supports:
- macOS (tested)
- GNOME Linux (untested)
- KDE Plasma Linux (untested)
- XFCE Linux (untested)
- MATE Linux (untested)
If you have one of the untested OS, and it works, please let me know. If you have an OS that is not on the list, feel free to suggest it!

# Features
- Generates a color palette from any image.
- Color palette are guaranteed to be readable with good contrast.
- Assigned color roles. No more guessing which color does want with the palette.
- Sets wallpaper to your image automatically.
- Uses templates so that you can apply the color palette to your entire system.
- Supports program refreshing. No more closing and reopening programs to get them to update their palette.
- Options to increase color variety for palette. Useful for monochromatic images.

## Comparison
Here is a table that compares PaletteSnap with pywal:
|                               |      **pywal**     |   **PaletteSnap**  |
|:-----------------------------:|:------------------:|:------------------:|
|       **Palette Generation**      | :white_check_mark: | :white_check_mark: |
|     **Wallpaper Setting**     | :white_check_mark: | :white_check_mark: |
|         **Templating**        | :white_check_mark: | :white_check_mark: |
|      **Readable Palette**     |      :warning:     | :white_check_mark: |
| **More Color Variety Option** |         :x:        | :white_check_mark: |
|     **Refreshes Programs**    |         :x:        | :white_check_mark: |
|  **Custom background color**  | :white_check_mark: |         :x:        |
|    **Cached colorschemes**    | :white_check_mark: |         :x:        |
|       **Builtin themes**      | :white_check_mark: |         :x:        |
Note that many convenient features of pywal will be added to PaletteSnap in the future.

# Usage
When generating the palette, PaletteSnap creates two folders. On a macOS, they are
- `~/.config/palsnap/`
- `~/.cache/palsnap/`

This is very similar to what pywal does. For non-macOS systems, it generates the palsnap folders based on the `XDG_CONFIG_HOME` and `XDG_CACHE_HOME` environments.

## Palette Generation
To generate a palette, run the following command:
`palsnap gen <img_path>`
This is the simplest way to generate a palette. If you run `palsnap gen --help`, you'll notice there is a list of options:
- mode: theme mode (light/dark/auto)
- variety: color variety type (default/extra/mix)
- sample: number of colors to sample from image when finding accent color step
- mixAmount: amount to mix accent colors with chosen color for each iteration
- mixThreshold: distance threshold for colors until mixing stops
- weight: uniqueness weight for lighting optimization

`extra` introduces extra colors with color harmony to improve color variety in the palette. `mix` refines the color palette by mixing the chosen colors with the original colors (red, green, etc.) to try to make them as close as possible to a "standard" colorscheme.

If you keep hitting the *manual optimization* for your generated palette, this is usually a sign that your current options are not good. If you haven't already, an easy way to avoid it is to set your `mode` to either light or dark instead of auto.

### Preview
In order to preview a palette, you must first generate it. You can skip all the other steps in the process by running
`palsnap gen <img_path> --skip`. After that, run `palsnap preview` to preview the palette. The output will be the image (only for certain terminals) and all the colors. Your terminal window must be big enough to see all the colors. 

If you want a more direct approach, in the `~/.cache/palsnap` folder, there should be a `PaletteTest.html`. You can use it to see what your palette will actually look like if you use it.

## Templating
All templating information is done in `~/.config/palsnap/templates.toml`. Here is an example of what the file could look like:
```
[[sioyek]]
name = "sioyek.config"
alias = "prefs.config"
dir = "/Applications/sioyek.app/Contents/MacOS/"
cmd = ""

[[sketchybar]]
name = "sketchybarrc"
alias = ""
dir = "~/.config/sketchybar/"
cmd = "sketchybar --reload"
```
Explanations:
- `[[<process_name>]]` is the process name of the program. **It is important that the name corresponds to the program's process when opened**. If your program is open, running `pgrep -a <process_name>` should show a numerical ID.
- `name` is the name of the template file. It should include the file name extension and should be located in `~/.config/palsnap/templates` folder.
- `alias` is the name you want the template file to have upon generation.
- `dir` is the directory where the template file will generate in.
- `cmd` is the **refresh command**. Sometimes, you might want to change your colorscheme when some programs are open. PaletteSnap will run this shell command to refresh the program.

Once you set up the information about the template, you place your template in the `~/.config/palsnap/templates` folder. Variables in the template are represented as words surrounded by `{{` and `}}`. Here is a list of all the variables:
```
{{image}}
{{fg}}
{{bg0}}
{{bg1}}
{{bg2}}
{{bg3}}
{{bg4}}
{{bg5}}
{{black}}
{{red}}
{{orange}}
{{yellow}}
{{green}}
{{blue}}
{{cyan}}
{{magenta}}
{{violet}}
{{white}}
```
The variables are replaced with the corresponding colors in hex. For hex values without #, use something like `{{cyan.digits}}`. RGB colors can be represented as
```
{{magenta.r}} {{magenta.g}} {{magenta.b}}
```
Normalized rgb values are
```
{{magenta.nr}} {{magenta.ng}} {{magenta.nb}}
```

## Color Palette
Based on Everforest's palette usage,
| Identifier | Usages |
|---|---|
| `bg0` | Default Background |
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

# Supported Applications
PaletteSnap's flexibilty makes it possible for it to support any application with customizable colors. For sake of convenience, below are all the applications that are confirmed to work with their respective refresh commands, if needed:
| **Program** | **Command** |        **Additional Info**        |
|:-----------:|:-----------:|:---------------------------------:|
|   Wezterm   |      NA     | Wezterm auto refreshes its config |
|   Sioyek    |      NA     | Sioyek auto refreshes its config  |
|  Sketchybar |     `sketchybar --reload`        |  Sketchybar can auto refresh its config with hotloading.                                 |

This section will be expanded on with more detailed information.

# To Do
- Let users have more influence on palette output.
- Add wallpaper switching support for Linux distributions.
- Expand image preview capability to support more terminals.
-- Let users define number of background colors to influence the brightness of light/dark modes.
- Add custom background color support.
- Add caching to save time if user used same options in the past.
- Add folder support, allowing PaletteSnap to pick a wallpaper image randomly.

# Acknowledgments
- [pywal](https://github.com/dylanaraps/pywal) for the inspriation that led me to create PaletteSnap
- [ozwaldorf](https://github.com/ozwaldorf/) for helpful suggestions and advice during PaletteSnap's initial development. Check out [lutgen](https://github.com/ozwaldorf/lutgen-rs), a program that themes any image to a desktop colorscheme.
- [Everforest colorscheme](https://github.com/sainnhe/everforest/) for its colorscheme usage.
- [Solarized](https://github.com/altercation/solarized) and [Selenized](https://github.com/jan-warchol/selenized) colorschemes for giving me valuable insights on what a palette should be like.