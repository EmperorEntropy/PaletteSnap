###
# Modules
###
import os
import platform
import toml

###
# Identify the OS
###
osType = platform.system()

###
# Define program directories
###
# .config stores config files for PaletteSnap
# .cache stores the output

# Set up the environment
home = os.getenv('HOME', os.getenv('USERPROFILE'))
xdgCache = os.getenv('XDG_CACHE_HOME', os.path.join(home, '.cache'))
xdgConfig = os.getenv('XDG_CONFIG_HOME', os.path.join(home, '.config'))

# Define the directories
cache = os.path.join(xdgCache, 'palsnap')
config = os.path.join(xdgConfig, 'palsnap')
#module = os.path.dirname(__file__)

# Create the directories
os.makedirs(config, exist_ok=True)
os.makedirs(cache, exist_ok=True)

# Create palsnap.toml
defaultAccents = {
    "black": "#000000",
    "red": "#ff0000",
    "orange": "#ffa500",
    "yellow": "#ffff00",
    "green": "#008000",
    "blue": "#0000ff",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "violet": "#7f00ff",
    "white": "#ffffff"
}
palsnapFile = os.path.join(config, 'palsnap.toml')
if not os.path.isfile(palsnapFile):
    # create the file
    with open(palsnapFile, 'w') as file:
        # default accent colors
        toml.dump(defaultAccents, file)
    file.close()

# Create template.toml
templateFile = os.path.join(config, 'templates.toml')
if not os.path.isfile(templateFile):
    # create the file
    with open(templateFile, 'w') as file:
        pass
    file.close()

# Create the template folder
os.makedirs(os.path.join(config, 'templates'), exist_ok=True)
templateDir = os.path.join(config, 'templates')