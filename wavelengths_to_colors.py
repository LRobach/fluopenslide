"Gives the RGB color given by the wavelength."

import xml.etree.ElementTree as ET

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
    return([red, green, blue])


def getthewave (c):

    tree = ET.parse('meta.xml')
    root = tree.getroot()
    L = []

    for k in range(0,c): #modifier en mettant le nombre de canaux comme dans recolor_tile
        for child in root[0][4][3][12][0][k]:
            if child.tag=="EmissionWavelength" :
                a = float(child.text)
                L.append(WavelengthToColor(a))
    return(L)
