"Gives the RGB color given by the wavelength."

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import pathlib
import aicspylibczi

def WavelengthToColor (wavelength) :
    """
    Gives the RGB color corresponding to the wavelength.

    Parameter
    ---------
    wavelength : int
        The wavelength given in nanometer.

    Return
    ---------
    [R,G,B] : List
        The list of the RGB color, with R, G and B in [0,1].

    """
    if (wavelength == 0) :
        red = 1.0   # white light !!!
        green = 1.0 # white light !!!
        blue = 1.0  # white light !!!

    elif ((wavelength >= 1) and (wavelength < 380)) :
        red = 0.3
        green = 0.0
        blue = 0.3

    elif ((wavelength >= 380) and (wavelength < 440)) :
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0

    elif ((wavelength >= 440) and (wavelength < 490)) :
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0

    elif ((wavelength >= 490) and (wavelength < 510)) :
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)

    elif ((wavelength >= 510) and (wavelength < 540)) :
        red = (wavelength - 510) / (540 - 510)
        green = 1.0
        blue = 0.0

    elif ((wavelength >= 540) and (wavelength < 620)) :
        red = 1.0
        green = -(wavelength - 620) / (620 - 540)
        blue = 0.0

    elif ((wavelength >= 620) and (wavelength <= 680)) :
        red = 1.0
        green = 0.0
        blue = (wavelength - 620) / (680 - 620)

    elif ((wavelength > 680) and (wavelength < 3000)) :
        red = 0.3
        green = 0.0
        blue = 0.3

    else :
        red = 0.3
        green = 0.0
        blue = 0.3
    return([red, 0, 0], [0, green, 0], [0, 0, blue])


def get_the_wavelength (file, c):
    """
    Gives the RGB color of each channel.

    Parameter
    ---------
    c : int
        Number of channels present in the file.

    Return
    ---------
    L : List
        The list composed of the RGB colors of each channels.

    """
    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)
    root = czi.meta
    superroot = ElementTree(root)
    root = superroot.getroot()

    L = []

    for k in range(0,c):
        for child in root[0][4][3][12][0][k]:
            if child.tag=="EmissionWavelength" :
                a = float(child.text)
                L.append(WavelengthToColor(a))

    return(L)
