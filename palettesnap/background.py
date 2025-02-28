###
# Modules
###

# Internal Modules
from .colorClass import Color

# External Modules
import numpy as np

def findBgGradient(bgColor : Color, fgColor : Color) -> dict[str, Color]:
    '''returns a spectrum'''
    '''determines background accent'''
    bgDict = dict()
    # Get 5 gradient colors from background to foreground
    gradient = np.linspace(bgColor.oklab, fgColor.oklab, 7)
    gradient = [Color(*tuple(labColor)) for labColor in gradient]
    for i in range(1, 6):
        bgDict[f"bg{i}"] = gradient[i]
    return bgDict