""" By giving position, width, height in pixels,
you have access to the tiles needed to open your flurescence image."""

import pathlib
import aicspylibczi
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET


def size(file):
    """
    Find the dimension of the entire czi image.

    Parameter
    ---------
    file : str
        The name of your czi file

    Example
    ---------
    file = '/Users/louisonrobach/Documents/renom.czi'

    Return
    ---------
    Tuple [SizeX, SizeY]
        The size, in pixel, of your entire czi image.

    """
    L = []
    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)

    root = czi.meta
    superroot = ElementTree(root)
    root = superroot.getroot()

    for child in root[0][4][3]:
        if child.tag == "SizeX" or child.tag == "SizeY":
            L.append(float(child.text))

    return(L)


def tiles_to_open(file, x0, x1, y0, y1):
    """
    Create a list with the numbers of tiles to open.

    Parameters
    ---------
    file : str
       The name of your czi file
    x0 : positive int
        The number of pixel on x axis at the beggining of the image wanted.
    x1 : positive int
        The number of pixel on x axis at the end of the image wanted.
    y0 : positive int
        The number of pixel on y axis at the beggining of the image wanted.
    y1 : positive int
        The number of pixel on y axis at the end of the image wanted.

    Return
    ---------
    L : List
        A list of numbers representing the tiles
        to open to get the image wanted.

    """

    L = []

    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)

    # We supposed the dimensions of each file to open is : 'HSCMYX'
    t = czi.size
    pix = t[5]
    piy = t[4]
    [SizeX, SizeY] = size(file)
    column0 = x0//pix
    column1 = x1//pix
    line0 = y0//piy
    line1 = y1//piy
    nbXtile = SizeX//pix + 1

    for j in range(line0, line1 + 1):
        a = int(column0 + j * nbXtile)
        b = int(column1 + j * nbXtile)

        for k in range(a, b+1):
            L.append(k)

    return(L)
