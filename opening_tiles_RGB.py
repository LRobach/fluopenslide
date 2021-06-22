"Opening a czi file with RGB colors and read_image function."

from position_to_tile import tiles_to_open
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import aicspylibczi
from wavelength_to_color import get_the_wavelength


def norm_by(x, min_, max_):
    norms = np.percentile(x, [min_, max_])
    i2 = np.clip((x - norms[0]) / (norms[1] - norms[0]), 0, 1)
    return i2


def recolor_tile (file, n) :
    """
    Open the n tile and creates a numpy array colored in RGB.

    Parameters
    ---------
    file : str
       The path to your czi file.
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

    # On suppose que tous les fichiers à ouvrir ont la dim : 'HSCMYX'

    t = czi.size
    c = t[2]
    x = t[5]
    y = t[4]

    L = get_the_wavelength(c)

    image=np.zeros((x,y,3),dtype=float)

    for k in range (0,c):
        tuple_mosaic_data = czi.read_image(M=n, C=k, S=0, H=0)
        mosaic_data = tuple_mosaic_data[0] #on sélectionne uniquement le numpy.ndarray du tuple
        mosaic_data = mosaic_data[0,0,0,0,:,:]
        c1 = (norm_by(mosaic_data, 50, 99.8) * 255).astype(np.uint8)
        c2 = (norm_by(mosaic_data, 50, 99.8) * 255).astype(np.uint8)
        c3 = (norm_by(mosaic_data, 0, 100) * 255).astype(np.uint8)
        rgb = np.stack((c1, c2, c3), axis=2)

    # On recolore
        im_shape = np.array(rgb.shape)
        color_transform = np.array(L[k]).T
        im_reshape = rgb.reshape([np.prod(im_shape[0:2]), im_shape[2]]).T
        im_recolored = np.matmul(color_transform.T, im_reshape).T
        im_shape[2] = 3
        rgb = im_recolored.reshape(im_shape)
        mosaic_data = np.clip(rgb, 0, 255)
        mosaic_dataf = mosaic_data.astype(float) / 255.

        mosaic_dataf = edges(mosaic_dataf, x, y)

        image += mosaic_dataf

# On réalise une moyenne des couleurs pour supperposer correctement les couleurs sur les pixels ou plusieurs couches se superposent
    image /= 3.

    return(image)


def edges (image, x, y) :
    """
    Add zeros to the numpy array if it is an egde array.

    Parameters
    ---------
    image : numpy.array
        The tile recolored.
    x : int
        XSize of a tile created by the microscope.
    y : int
        YSize of a tile created by the microscope.

    Return
    ---------
    newim : numpy.array
        The numpy.array with (x,y) size, filled with 0 if image is smaller than newim.

    """

    if ( image.shape != (x, y, 3) ) :
        N = np.zeros ((x, y, 3))
        (a, b, c) = image.shape
        N[0:a, 0:b] = image
        return (N)
    return(image)


def final_array (file, x0, x1, y0, y1) :
    """
    Creates the final numpy array that contains all tiles colored in RGB.

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

    Return
    ---------
    N : np.array
        A numpy array that contains every tiles colored in RGB.

    """

    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)
    x = czi.size[5]
    y = czi.size[4]

    U = tiles_to_open(file, x0, x1, y0, y1)

    k = 0
    while ( U[k+1] == U[k]+1  and k < len(U)-2 ) :
        k = k+1
    a = k+1

    M=[]
    N = np.zeros ((int(len(U)/a)*y,int(a*x),3))

    for i in range (0, int(len(U)/a)) :
        for j in range (0, a) :
            image = recolor_tile(file, U[a*i+j])
            M.append(image)

    d = 0
    for i in range (0, int(len(U)/a)*y,y) :
        for j in range (0, a*x, x) :
            N[i:i+y, j:j+x] = M[d]
            d += 1

    return(N)


def size_from_tiles (file, x0, x1, y0, y1) :
    """
    Gives the distance from the edge of the tiles where the image is.

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

    Return
    ---------
    [x2, x3, y2, y3] : List
        The list containing the x and y position of the image in the surrounding tiles.

    """
    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)

    # On suppose que tous les fichiers à ouvrir ont la dim : 'HSCMYX'
    t = czi.size
    pix = t[5]
    piy = t[4]

    x2 = x0%pix
    y2 = y0%piy
    x3 = x2 + (x1-x0)
    y3 = y2 + (y1-y0)
    return([x2, x3, y2, y3])


def display_image (file, x0, x1, y0, y1) :
    """
    Display the RGB image with the position in file wanted.

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

    Return
    ---------
    An image created by matplotlib corresponding to the image wanted.
    """

    N = final_array(file, x0, x1, y0, y1)

    [x2,x3,y2,y3] = size_from_tiles (file, x0, x1, y0, y1)

    N = N[y2:y3, x2:x3]

    plt.imshow(N)
    plt.axis('on')
    plt.show()
