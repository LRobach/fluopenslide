"Opening a czi file without RGB colors and read_image function."

from position_to_tile import tiles_to_open
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import aicspylibczi


def creates_numpy_array (file, n) :
    """
    Open the n tile and creates a numpy array.

    Parameters
    ---------
    file : str
       The path to your czi file
    n : int

    Example
    ---------
    file = '/Users/louisonrobach/Documents/renom.czi'

    Return
    ---------
    M : np.array
        A numpy array that represents the colorization in RGB colors of the n tile.

    """
    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)

    # We supposed the dimensions of each file to open is : 'HSCMYX'
    t = czi.size
    c = t[2]
    x = t[5]
    y = t[4]

    image=np.zeros((x,y,3),dtype=float)

    for k in range (0,c):
        tuple_mosaic_data = czi.read_image(M=n, C=k, S=0, H=0)
        mosaic_data = tuple_mosaic_data[0] # We want only the numpy.darray and it is a tuple
        mosaic_data = mosaic_data[0,0,0,0,:,:]
        image += mosaic_data

    image /= 3.

    return(image)


def final_array_2 (file, x0, x1, y0, y1) :
    """
    Creates the final numpy array that contains all tiles colored in RGB.

    Parameters
    ---------
    file : str
       The path to your czi file
    x0 : int
        The number of pixel on x axis at the beggining of the image wanted.
    x1 : int
        The number of pixel on x axis at the end of the image wanted.
    y0 : int
        The number of pixel on y axis at the beggining of the image wanted.
    y1 : int
        The number of pixel on y axis at the end of the image wanted.

    Example
    ---------
    file = '/Users/louisonrobach/Documents/renom.czi'

    Return
    ---------
    N : np.array
        A numpy array that contains every tiles colored in RGB.

    """

    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)
    x = czi.size[5]
    y = czi.size[4]

    L = tiles_to_open(file, x0, x1, y0, y1)

    k = 0
    while ( L[k+1] == L[k]+1  and k < len(L)-2 ) :
        k = k+1
    a = k+1

    M=[]
    N = np.zeros ((int(len(L)/a)*y,a*x,3))

    for i in range (0, int(len(L)/a)) :
        for j in range (0, a) :
            image = creates_numpy_array(file, L[a*i+j])
            M.append(image)

    d = 0
    for i in range (0, int(len(L)/a)*y,y) :
        for j in range (0, a*x, x) :
            N[i:i+y, j:j+x] = M[d]
            d += 1

    return(N)


def creates_non_RGB_array (file, x0, x1, y0, y1) :
    """
    Creates the numpy array containing the non RGB image.

    Parameters
    ---------
    file : str
       The path to your czi file.
    x0 : int
        The number of pixel on x axis at the beggining of the image wanted.
    x1 : int
        The number of pixel on x axis at the end of the image wanted.
    y0 : int
        The number of pixel on y axis at the beggining of the image wanted.
    y1 : int
        The number of pixel on y axis at the end of the image wanted.

    Example
    ---------
    file = '/Users/louisonrobach/Documents/renom.czi'

    """

    N = final_array_2(file, x0, x1, y0, y1)
