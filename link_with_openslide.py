from opening_with_pyramid_level import get_array
import pathlib
import aicspylibczi
from position_to_tile import size


class KillOpenSlide():
    """
    The KillOpenSlide object try to behave like the OpenSlide one.
    The present functions have similar interests than OpenSlide ones,
    and so similar names.
    """

    def __init__(self, file):
        """
        Open the .czi file.

        Parameter
        ---------
        file : str
           The path to your czi file.

        """
        self.path = file

        mosaic_file = pathlib.Path(self.path)
        czi = aicspylibczi.CziFile(mosaic_file)
        self.file = czi

    def data(self):
        """
        Give information about the file. Returns a list : [[SizeX, SizeY],
        number of tiles, [tileSizeX, tileSizeY]].

        """
        t = self.file.size
        return([size(self.path), t[3], [t[5], t[4]]])

    def level_count(self):
        """
        Give the number of levels in the image.
        This number is not real, because there is an infinity of levels
        accessible with the scale_factor.

        """
        return(10)

    def levels(self):
        """
        Give a list containing the different levels of the image.

        """
        return sorted([1./(2**k) for k in range(10)])

    def level_dimensions(self, location, size):
        """
        A list of (width, height) tuples, one for each level of the image.

        """
        L = []
        x, y = location
        w, h = size
        for k in self.levels:
            mosaic_data = self.file.read_mosaic(
                (x, y, w, h), scale_factor=k, C=0
            )
            mosaic_data = mosaic_data[0, :, :]
            L.append(mosaic_data.shape)
        return(L)

    def read_region(self, location, level, size):
        """
        Display the image with the same arguments than used with openslide.

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

        return (get_array(self.path, x, x+w, y, y+h, level/(2**level)))
