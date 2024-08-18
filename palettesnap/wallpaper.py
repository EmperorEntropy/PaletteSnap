###
# Modules
###

# External modules
import os
import subprocess

# Interal modules
from . import setup
from .console import console

###
# Helper functions
###
def untestWarn() -> None:
    '''prints the untested warning message to console'''
    console.log("You are using one of the untested OS or Linux environments.")
    console.log("Please let the creator know if it works or not.")
    return None

def findEnv():
    '''return the desktop environment'''
    env = os.getenv('XDG_CURRENT_DESKTOP', '')
    if "GNOME" in env:
        return "GNOME"
    elif "KDE" in env:
        return "KDE"
    elif "XFCE" in env:
        return "XFCE"
    elif "MATE" in env:
        return "MATE"
    else:
        return None

def setMacWallpaper(imgPath):
    '''set the wallpaper for macOS'''
    subprocess.run(['osascript', '-e', 'tell application \"System Events\" to tell every desktop to set picture to \"%s\" as POSIX file' % imgPath])

# based off pywal's https://raw.githubusercontent.com/dylanaraps/pywal/master/pywal/wallpaper.py
def setLinuxWallpaper(env, imgPath):
    '''set the wallpaper for Linux'''
    if env == "GNOME":
        untestWarn()
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', f'file://{imgPath}'])
    elif env == "KDE":
        kdeCommand = [
            "qdbus", 
            "org.kde.plasmashell", 
            "/PlasmaShell", 
            "org.kde.PlasmaShell.evaluateScript",
            f'var allDesktops = desktops();print (allDesktops);for (i=0;i<allDesktops.length;i++) {{d = allDesktops[i];d.wallpaperPlugin = "org.kde.image";d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");d.writeConfig("Image", "file://{imgPath}")}}'
        ]
        subprocess.run(kdeCommand, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif env == "XFCE":
        untestWarn()
        subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-p', '/backdrop/screen0/monitor0/image-path', '-s', imgPath])
    elif env == "MATE":
        untestWarn()
        subprocess.run(['dconf', 'write', '/org/mate/desktop/background/picture-filename', f"'{imgPath}'"])

#####
# Main function
#####
def setWallpaper(path):
    '''set the wallpaper for all systems'''
    osType = setup.osType
    console.log("Setting new wallpaper.")
    if osType == 'Darwin':
        setMacWallpaper(path)
        console.log(f"Wallpaper succesfully set to [u]{path}[/u].")
    elif osType == 'Linux':
        env = findEnv()
        if env:
            setLinuxWallpaper(env, path)
            console.log(f"Wallpaper succesfully set to [u]{path}[/u] for {env}.")
        else:
            console.log("Could not identify desktop environment. [red]Failed[/red] to set wallpaper.")
    else:
        console.log(f"{osType} OS not supported. [red]Failed[/red] to set wallpaper.")