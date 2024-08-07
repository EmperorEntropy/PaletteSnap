###
# Modules
###
import numpy as np
from colour import Oklab_to_XYZ, XYZ_to_sRGB, RGB_to_HSL, sRGB_to_XYZ, XYZ_to_Lab, XYZ_to_Oklab, Lab_to_XYZ, HSL_to_RGB
from PIL import ImageColor

###
# Helper functions
###
def okToNormalRgb(okColor):
    '''oklab color to rgb normalized'''
    xyzColor = Oklab_to_XYZ(list(okColor))
    rgbColor = XYZ_to_sRGB(xyzColor)
    red, green, blue = tuple(rgbColor)
    # Clamp color values to eliminate impossible colors
    [red, green, blue] = np.clip([red, green, blue], 0, 1)
    return (red, green, blue)

def normalRgbToRgb(rgbColor):
    '''normalized rgb to rgb'''
    red, green, blue = rgbColor
    red = round(red * 255)
    green = round(green * 255)
    blue = round(blue * 255)
    return (red, green, blue)

def normalRgbToHex(rgbColor):
    '''normalized rgb to hex'''
    red, green, blue = normalRgbToRgb(rgbColor)
    return "#{:02x}{:02x}{:02x}".format(red,green,blue)

def normalRgbToHsl(rgbColor):
    '''normalized rgb to hsl'''
    hslColor = RGB_to_HSL(rgbColor)
    hue, saturation, light = tuple(hslColor)
    hue = round(hue * 360)
    saturation = round(saturation * 100)
    light = round(light * 100)
    return (hue, saturation, light)


def normalRgbToCIE(rgbColor):
    '''normalized rgb to cielab'''
    xyzColor = sRGB_to_XYZ(list(rgbColor))
    cieColor = XYZ_to_Lab(xyzColor)
    return cieColor

# used for palette extraction
def hexToLab(hexColor):
    '''converts hex to lab color'''
    red, green, blue = ImageColor.getcolor(hexColor, "RGB")
    red /= 255
    green /= 255
    blue /= 255
    xyzColors = sRGB_to_XYZ([red, green, blue])
    labColors = XYZ_to_Oklab(xyzColors)
    return tuple(labColors)

# used for palette extraction
def hslColor(hslColor):
    hue, saturation, light = hslColor
    hue /= 360
    saturation /= 100
    light /= 100
    rgbColor = HSL_to_RGB([hue, saturation, light])
    xyzColor = sRGB_to_XYZ(rgbColor)
    labColor = tuple(XYZ_to_Oklab(xyzColor))
    return Color(*labColor)

# used for optimization
def cieColor(currColor):
    '''CIE Lab color as tuple to Color class'''
    xyzColor = Lab_to_XYZ(list(currColor))
    okLab = tuple(XYZ_to_Oklab(xyzColor))
    okColor = Color(*okLab)
    return okColor

# used for palette extraction
def rgbColor(rgbColor):
    '''rgb color to Color'''
    red, green, blue = rgbColor
    red /= 255
    green /= 255
    blue /= 255
    xyzColor = sRGB_to_XYZ([red, green, blue])
    labColor = tuple(XYZ_to_Oklab(xyzColor))
    return Color(*labColor)

# use for palette extraction
def hexColor(hexColor):
    '''hex color to Color'''
    red, green, blue = ImageColor.getcolor(hexColor, "RGB")
    red /= 255
    green /= 255
    blue /= 255
    xyzColors = sRGB_to_XYZ([red, green, blue])
    labColors = tuple(XYZ_to_Oklab(xyzColors))
    return Color(*labColors)

# used for previewing
def hexToRgb(hexColor):
    red, green, blue = ImageColor.getcolor(hexColor, "RGB")
    return (red, green, blue)

###
# Color class
###
class Color():

    def __init__(self, L, a, b):
        '''Initialize Oklab color'''
        self.L = L
        self.a = a
        self.b = b
        # different color spaces
        self.oklab = (L, a, b)
        self.normalRgb = okToNormalRgb(self.oklab)
        self.rgb = normalRgbToRgb(self.normalRgb)
        # we use rgb since rgb eliminates impossible colors
        self.hex = normalRgbToHex(self.normalRgb)
        self.hsl = normalRgbToHsl(self.normalRgb)
        self.cielab = normalRgbToCIE(self.normalRgb)

    def __repr__(self):
        '''string representation'''
        red, green, blue = self.rgb
        return f"{self.hex} \033[48;2;{red};{green};{blue}m   \033[0m"
    
    def findDist(self, other):
        '''computes distance btw two colors'''
        return ((self.L - other.L)**2+(self.a - other.a)**2+(self.b - other.b)**2)**0.5

