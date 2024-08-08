###
# Modules
###

# External modules
import subprocess
import requests

# Internal modules
from .console import console

###
# Main functions
###
def findCurrVersion() -> str:
    '''returns user-installed version'''
    res = subprocess.run(['pip', 'show', 'palettesnap'], capture_output=True).stdout.decode("utf-8")
    version = res.splitlines()[1]
    version = version.split(" ")[1]
    return version

def findLatestVersion() -> str | None:
    '''returns latest version on PyPi'''
    url = "https://pypi.org/pypi/palettesnap/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        version = response.json()["info"]["version"]
        return version
    except requests.exceptions.HTTPError:
        return None

def outdatedCheck() -> None:
    '''check if user-installed version is outdated or not'''
    current = findCurrVersion()
    latest = findLatestVersion()
    if latest == None:
        console.log("Failed to check for palettesnap updates.")
    elif current != latest:
        console.log("Your version of palettesnap is [red]outdated[/red].")
        console.log(f"Current version: {current}.")
        console.log(f"Latest version: {latest}.")
    else:
        console.log("Your version of palettesnap is [green]up-to-date[/green].")