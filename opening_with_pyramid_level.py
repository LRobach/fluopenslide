"Opening a czi file with RGB colors and read_mosaic function."

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


def open_image (file, x0, x1, y0, y1, level) :
    """
    Display the image wanted with the read_mosaic function. With this function, you are able to choose the pyramid level.

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
    level : int
        The level of the pyramid wanted. Between 0 and 1.

    Example
    ---------
    file = '/Users/louisonrobach/Documents/renom.czi'

    Return
    ---------
    An image created by matplotlib corresponding to the image wanted.
    """

    mosaic_file = pathlib.Path(file)
    czi = aicspylibczi.CziFile(mosaic_file)

    # On suppose que tous les fichiers à ouvrir ont la dim : 'HSCMYX'

    t = czi.size
    c = t[2]
    x = t[5]
    y = t[4]

    L = get_the_wavelength(file, c)

    mosaic_data = czi.read_mosaic((x0,y0,x1-x0,y1-y0), scale_factor=level, C=0)
    mosaic_data = mosaic_data[0,:,:]
    c1 = (norm_by(mosaic_data, 50, 99.8) * 255).astype(np.uint8)
    c2 = (norm_by(mosaic_data, 50, 99.8) * 255).astype(np.uint8)
    c3 = (norm_by(mosaic_data, 0, 100) * 255).astype(np.uint8)
    rgb = np.stack((c1, c2, c3), axis=2)

# On recolore
    im_shape = np.array(rgb.shape)
    color_transform = np.array(L[0]).T
    im_reshape = rgb.reshape([np.prod(im_shape[0:2]), im_shape[2]]).T
    im_recolored = np.matmul(color_transform.T, im_reshape).T
    im_shape[2] = 3
    rgb = im_recolored.reshape(im_shape)
    mosaic_data = np.clip(rgb, 0, 255)
    mosaic_dataf = mosaic_data.astype(float) / 255.

    (x, y, v) = mosaic_dataf.shape

    image = np.zeros((x,y,3),dtype=float)

    image += mosaic_dataf

    for k in range (1,c):
        mosaic_data = czi.read_mosaic((x0,y0,x1-x0,y1-y0), scale_factor=level, C=k)
        mosaic_data = mosaic_data[0,:,:]
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

    image /= 3.

    plt.imshow(image)
    plt.axis('on')
    plt.show()
