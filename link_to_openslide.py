from opening_with_pyramid_level import open_image
import pathlib
import aicspylibczi


class KillOpenSlide() :
    """
    The KillOpenSlide object try to behave like the OpenSlide one.
    The present functions have similar interests than OpenSlide ones, and so similar names.
    """

    def __init__ (self, file) :
        """
        Open the .czi file.

        Parameter
        ---------
        file : str
           The path to your czi file.

        """
        self.path = file


    def read_region (self, location, level, size) :
        """
        Display the image by giving the same arguments than used with openslide.

        Parameters
        ---------
        location = (x, y) : tuple
            tuple giving the top left pixel of the image wanted.
        level : int
            the level number.
        size = (width, height) : tuple
            tuple giving the size of the image.

        Return
        ---------
        The image wanted.

        """

        (x, y) = location
        (w, h) = size

        return(open_image (self.path, x, x+w, y, y+h, level/(2**level)) # On suppose que le niveau le plus haut de la pyramide est 8.
