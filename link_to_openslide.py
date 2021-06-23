from opening_with_pyramid_level import get_array
import pathlib
import aicspylibczi
from position_to_tile import size

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

    def data (self) :
        """
        Gives information about the file. Returns a list : [[SizeX, SizeY], number of tiles, [tileSizeX, tileSizeY]].

        """
        mosaic_file = pathlib.Path(self.path)
        czi = aicspylibczi.CziFile(mosaic_file)
        t = czi.size
        return([size(self.path), t[3], [t[5], t[4]]])

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

        """

        (x, y) = location
        (w, h) = size

        return (get_array (self.path, x, x+w, y, y+h, level/(2**level)))
