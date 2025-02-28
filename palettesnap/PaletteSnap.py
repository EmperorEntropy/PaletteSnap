###
# Modules
###

# Internal Modules
from . import setup
from .colorOptimize import performOptimal
from .console import console
from .colorClass import Color, rgbColor, hexColor, lchColor
from .background import findBgGradient

# External Modules
import numpy as np
import numpy.typing as npt
#import sklearn
from pykdtree.kdtree import KDTree
from kmedoids import fasterpam
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from colour import read_image, sRGB_to_XYZ, XYZ_to_Oklab
import concurrent.futures
import mixbox
import os
import toml

# Use python3 -m pip
# We use the Oklab colorspace

###
# Config Functions
###

def isValidHex(hexString : str) -> bool:
    '''returns true if string is valid hex'''
    # expand on this later
    return len(hexString) == 7

def parseConfig() -> dict[str, Color]:
    '''parses palsnap.toml'''
    console.log("Defined accent colors:")
    accentDict = toml.load(setup.palsnapFile)
    # double check values
    for key, value in accentDict.items():
        if not isValidHex(value):
            raise Exception("palsnap.toml is wrong")
    accentDict = {key : hexColor(value) for key, value in accentDict.items()}
    console.log(accentDict)
    return accentDict

###
# Finder Functions
##
def findBackground(labColors : npt.NDArray[any], mode : str, dominant : int) -> Color:
    '''returns the background color for the palette'''
    if mode == "auto":
        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=1)
        kmeans.fit(labColors)
        bgColors = kmeans.cluster_centers_
        bgColors = tuple(bgColors[0])
        return Color(*bgColors)
    else:
        # Apply KMeans clustering
        console.log(f"Using {dominant} dominant colors to find {mode} background color.")
        kmeans = KMeans(n_clusters=dominant)
        kmeans.fit(labColors)
        bgColors = kmeans.cluster_centers_
        bgColors = [tuple(labColor) for labColor in bgColors]
        bgColors = sorted(bgColors, key=lambda x: x[0])
        if mode == "dark":
            return Color(*bgColors[0])
        else:
            return Color(*bgColors[-1])

def findForeground(bgColor : Color, labColors : npt.NDArray[any]) -> Color:
    '''returns the foreground color for the palette'''
    L = bgColor.L
    threshold = 0.33
    # Filter out the bad colors
    filterArray = np.where(abs(labColors[:,0]-L) > threshold, True, False)
    goodColors = labColors[filterArray]
    if goodColors.size == 0:
        raise Exception("No foreground found. Please lower threshold.")
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(goodColors)
    fgColor = kmeans.cluster_centers_
    fgColor = tuple(fgColor[0])
    fgColor = Color(*fgColor)
    return fgColor

def filterColors(labColors : npt.NDArray[any], specialColor : tuple[int | float, int | float, int | float], numSample : int) -> Color:
    '''filter colors in image based on a color'''
    L, a, b = specialColor
    specialColor = np.asarray([[L, a, b]])
    # Filter to find a certain number of the most similar colors
    kd_tree = KDTree(labColors)
    dist, idx = kd_tree.query(specialColor, k=numSample)
    filteredColors = labColors[idx]
    # Eliminate channels
    height, width, channels = filteredColors.shape
    filteredColors = filteredColors.reshape((height * width, channels))
    # Use KMedoids to find best one out of the sampled colors
    distMatrix = pairwise_distances(filteredColors, filteredColors)
    dominantIdx = fasterpam(distMatrix, 1)
    finalColor = tuple(filteredColors[dominantIdx.medoids][0])
    # Convert to Color
    return Color(*finalColor)

def findAccentColors(labColors : npt.NDArray[any], extraDict : dict[str, Color], numSample : int) -> dict[str, Color]:
    '''finds the accent colors'''
    resDict = dict()
    values = [(key, value.oklab) for key, value in extraDict.items()]
    # Get the extra colors in parallel
    futureDict = dict()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Find the futures
        for key, value in values:
            future = executor.submit(filterColors, labColors, value, numSample)
            futureDict[future] = key
        # Process result
        for future in concurrent.futures.as_completed(futureDict):
            key = futureDict[future]
            result = future.result()
            resDict[key] = result
    # Rearrange key ordering
    keyOrder = list(extraDict.keys())
    resDict = {key : resDict[key] for key in keyOrder}
    return resDict

def findColorHarmony(givenColor : Color) -> dict[str, Color]:
    '''finds colors that are harmonious with the given color'''
    # use Oklch color space
    light, chroma, hue = givenColor.oklch
    harmonyColors = dict()
    # complementary
    comHue = (hue + 180) % 360
    complementaryColor = (light, chroma, comHue)
    harmonyColors["complementary"] = lchColor(complementaryColor)
    # analogous
    angHue1 = (hue + 30) % 360
    angHue2 = (hue - 30) % 360
    ang1 = (light, chroma, angHue1)
    ang2 = (light, chroma, angHue2)
    harmonyColors["analogous 1"] = lchColor(ang1)
    harmonyColors["analogous 2"] = lchColor(ang2)
    # split complementary
    splitHue1 = (hue + 150) % 360
    splitHue2 = (hue + 210) % 360
    split1 = (light, chroma, splitHue1)
    split2 = (light, chroma, splitHue2)
    harmonyColors["split complementary 1"] = lchColor(split1)
    harmonyColors["split complementary 2"] = lchColor(split2)
    # triadic
    triHue1 = (hue + 120) % 360
    triHue2 = (hue + 240) % 360
    tri1 = (light, chroma, triHue1)
    tri2 = (light, chroma, triHue2)
    harmonyColors["triadic 1"] = lchColor(tri1)
    harmonyColors["triadic 2"] = lchColor(tri2)
    # square (og, 90, 180, 270)
    squareHue1 = (hue + 90) % 360
    squareHue2 = (hue + 270) % 360
    sq1 = (light, chroma, squareHue1)
    sq2 = (light, chroma, squareHue2)
    harmonyColors["square 1"] = lchColor(sq1)
    harmonyColors["square 2"] = lchColor(sq2)
    # tetradic (og, 60, 180, 240)
    tetraHue1 = (hue + 60) % 360
    tetraHue2 = (hue + 240) % 360
    tetra1 = (light, chroma, tetraHue1)
    tetra2 = (light, chroma, tetraHue2)
    harmonyColors["tetradic 1"] = lchColor(tetra1)
    harmonyColors["tetradic 2"] = lchColor(tetra2)
    return harmonyColors

def findMode(bgColor : Color) -> str:
    '''finds the mode of the palette if given mode is auto'''
    if bgColor.L >= 0.5:
        return "light"
    else:
        return "dark"

###
# Manipulation Functions
###
def processImage(imgPath : str) -> npt.NDArray[any]:
    '''processes the image and returns an array of Oklab colors'''
    # Get the colors
    console.log(f"Reading image [u]{imgPath}[/u].")
    imgPath = os.path.expanduser(imgPath)
    rgbColors = read_image(imgPath, method="Imageio")
    rgbColors = rgbColors[..., 0:3]
    # Convert colors to Oklab color space
    console.log("Converting image colors to [cyan]Oklab[/cyan] color space.")
    xyzColors = sRGB_to_XYZ(rgbColors)
    labColors = XYZ_to_Oklab(xyzColors)
    labColors = labColors.reshape((-1,3))
    return labColors

def adjustAccents(colorDict : dict[str, Color], iterations : int, weight : int) -> dict[str, Color]:
    '''adjusts lightness of accents based on background'''
    # based on https://github.com/jan-warchol/selenized/blob/master/balancing-lightness-of-colors.md
    bgLightness = colorDict["bg"].cielab[0]
    # adjust the lightness
    newAccents = performOptimal(bgLightness, colorDict, iterations, weight)
    return newAccents

def findClosestColor(colorDict : dict[str, Color], labColor : Color) -> str:
    '''finds the color name in colorDict that labColor is closest to'''
    # find the best color name
    bestColor = None
    bestDist = float("inf")
    for (key, otherColor) in colorDict.items():
        distance = Color.findDist(labColor, otherColor)
        if distance < bestDist:
            bestDist = distance
            bestColor = key
    return bestColor

def tweakColor(paletteColor : Color, orgColor : Color, hueThreshold, hueFactor, chromaThreshold, chromaFactor) -> Color:
    '''tweaks the chroma and hue of the color so that it is closer to the accent colors'''
    orgHue = orgColor.oklch[2]
    paletteHue = paletteColor.oklch[2]
    orgChroma = orgColor.oklch[1]
    paletteChroma = paletteColor.oklch[1]
    # change hue
    if abs(orgHue - paletteHue) > hueThreshold:
        newHue = orgHue * hueFactor
    else:
        newHue = paletteHue
    # change chroma
    if paletteChroma * chromaThreshold <= orgChroma:
        newChroma = orgChroma * chromaFactor
    else:
        newChroma = paletteChroma
    return lchColor((paletteColor.oklch[0], newChroma, newHue))

###
# Palette Functions
###
def pickColors(imgPath : str, accentColors : dict[str, Color], mode : str, dominant : int, numSample : int) -> dict[str, Color]:
    '''start picking colors from the image'''
    palette = dict()
    labColors = processImage(imgPath)
    # Background
    console.log("Finding background color.")
    bg = findBackground(labColors, mode, dominant)
    palette["bg"] = bg
    # Foreground
    console.log("Finding foreground color.")
    fg = findForeground(bg, labColors)
    palette["fg"] = fg
    # Accents
    console.log(f"Finding accents by sampling [magenta]{numSample} colors[/magenta].")
    accentColors = findAccentColors(labColors, accentColors, numSample)
    palette |= accentColors
    return palette

def expandPalette(accentColors : dict[str, Color], givenColor : Color, palette : dict[str, list[Color]]) -> dict[str, list[Color]]:
    '''expand the modified palette with a given color by finding the corresponding label via accentColors'''
    harmonyColors = findColorHarmony(givenColor)
    # find closest color for each of the harmony colors and expand the palette
    for key in harmonyColors:
        # find the closest label
        currColor = harmonyColors[key]
        label = findClosestColor(accentColors, currColor)
        # expand the palette
        palette[label].append(currColor)
    return palette

def exportPalette(colorDict : dict[str, Color]) -> None:
    '''exports the palette'''
    strDict = {key: value for key, value in colorDict.items() if key == "image" or key == "mode"}
    colorDict : dict[str, str] = {key : value.hex for key, value in colorDict.items() if key != "image" and key != "mode"}
    colorDict = strDict | colorDict
    exportPath = os.path.join(setup.cache, "palette.toml")
    with open(exportPath, "w") as file:
        toml.dump(colorDict, file)
    file.close()

def mixPalette(accentColors : dict[str, Color], palette : dict[str, Color], mixAmount : float, mixThreshold : float) -> dict[str, Color]:
    '''mixes colors in palette with accent colors'''
    console.log(f"Mixing colors to increase color variety.")
    console.log(f"Mixing colors by {mixAmount * 100}% each iteration with threshold distance {mixThreshold}.")
    numNeeded = len(accentColors.keys())
    passed = set()
    counter = 0
    while len(passed) != numNeeded:
        for key in accentColors:
            counter += 1
            paletteColor = palette[key].rgb
            accentColor = accentColors[key].rgb
            distance = Color.findDist(palette[key], accentColors[key])
            # only mix by 10% if distance > 0.16
            if distance > mixThreshold:
                mixedColor = mixbox.lerp(paletteColor, accentColor, mixAmount)
                # set mixed colors in palette
                mixedColor = rgbColor(mixedColor)
                palette[key] = mixedColor
            else:
                passed.add(key)
    console.log(f"Mixed a total of {counter} times.")
    return palette

###
# Main Function
###
def extractPalette(imgPath : str, mode : str, dominant : int, extraFlag : bool, mixFlag : bool, tweakFlag : bool,  
                   numSample : int, mixAmount : float, mixThreshold : float, iterations : int, weight : int, 
                   hueThreshold, hueFactor, chromaThreshold, chromaFactor, adjust : bool) -> dict[str, Color]:
    '''extracts the palette from the image'''
    # Get the accent values
    console.log("Reading [u]palsnap.toml[/u].")
    accentColors = parseConfig()

    console.log("Extracting palette.")
    palette = pickColors(imgPath, accentColors, mode, dominant, numSample)

    # harmony colors
    if extraFlag:
        console.log("Finding extra colors to improve color variety.")
        bgColor = palette["bg"]
        fgColor = palette["fg"]
        palette = {key: [value] for key, value in palette.items()}
        console.log("Getting colors harmonious to background.")
        paletteExpanded = expandPalette(accentColors, bgColor, palette)
        console.log("Getting colors harmonious to foreground.")
        paletteExpanded = expandPalette(accentColors, fgColor, paletteExpanded)
        # pick the color in the expanded palette with the least difference
        for key in paletteExpanded:
            possibleColors = paletteExpanded[key]
            if len(possibleColors) == 1:
                paletteExpanded[key] = possibleColors[0]
            else:
                orgColor = accentColors[key]
                # find the best lab color
                bestColor = None
                bestDist = float("inf")
                for currColor in possibleColors:
                    distance = Color.findDist(orgColor, currColor)
                    if distance < bestDist:
                        bestColor = currColor
                        bestDist = distance
                paletteExpanded[key] = bestColor
        # overwrite palette
        palette : dict[str, Color] = paletteExpanded

    # mixing
    if mixFlag:
        palette = mixPalette(accentColors, palette, mixAmount, mixThreshold)

    # tweak colors
    if tweakFlag:
        console.log("Tweaking colors.")
        for key in accentColors:
            newColor = tweakColor(palette[key], accentColors[key], hueThreshold, hueFactor, chromaThreshold, chromaFactor)
            palette[key] = newColor

    # adjusting
    if adjust:
        console.log(f"Adjusting palette with uniqueness weight {weight}.")
        newPalette = adjustAccents(palette, iterations, weight)
        palette = {**palette, **newPalette}

    # add image path and mode
    palette["image"] = imgPath
    if mode == "auto":
        palette["mode"] = findMode(palette["bg"])
    else:
        palette["mode"] = mode

    # generate background gradient
    console.log("Generating background gradient.")
    bgGradient = findBgGradient(palette["bg"], palette["fg"])
    palette |= bgGradient

    # reorder palette
    bgOrder = ['image', 'mode', 'bg', 'fg', 'bg1', 'bg2', 'bg3', 'bg4', 'bg5']
    reorderPalette = {key: palette[key] for key in bgOrder}
    reorderPalette.update({key: value for key, value in palette.items() if key not in reorderPalette})
    palette = reorderPalette

    # display palette
    console.log("Final palette:")
    console.log(palette)

    # export palette for preview
    console.log("Exporting palette.")
    exportPalette(palette)

    return palette