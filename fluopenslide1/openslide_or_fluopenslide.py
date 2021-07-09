from fluopenslide import FluOpenSlide
from openslide import OpenSlide
import os


L = [
    '.mrxs', '.svs', '.tif', '.ndpi', '.vms', '.vmu',
    '.scn', '.tiff', '.svslide', '.bif'
]


class OpenslideObject(Exception):
    """
    The object created can be opened with OpenSlide.
    """
    pass


class FluOpenSlideObject(Exception):
    """
    The object created can be opened with FluOpenSlide.
    """
    pass


class Unknown(Exception):
    """
    The object can not be opened.
    """
    pass


class choice(FluOpenSlide, OpenSlide):
    """
    Decide witch program use between OpenSlide and FluOpenSlide.

    """
    def __init__(self, file, choice=None):
        """
        Parameters
        ---------
        file : str
           The path to your czi file.
        choice : str
            Have to be "FluOpenSlide" or "Openslide".
            If there is no choice, focus on the file extension.
        """
        self.name, self.extension = os.path.splitext(file)

        if (choice == "FluOpenSlide" or choice == "fluopenslide"):
            FluOpenSlide.__init__(self, file)
            self = FluOpenSlide(file)
            raise FluOpenSlideObject(
                'Le fichier est à présent un objet FluOpenSlide.'
            )
        if (choice == "Openslide" or choice == "openslide"):
            OpenSlide.__init__(self, file)
            self = Openslide(file)
            raise OpenslideObject(
                'Le fichier est à présent un objet OpenSlide.'
            )
        if choice is None:
            print(
                "Aucune ouverture spécifique du fichier"
                "n'a été demandée.\n"
                "Par conséquent, "
                "nous allons nous baser sur l'extension du fichier."
            )
            if (self.extension == '.czi'):
                FluOpenSlide.__init__(self, file)
                self = FluOpenSlide(file)
                raise FluOpenSlideObject("L'objet est un FluOpenSlide.")
            if (self.extension in L):
                OpenSlide.__init__(self, file)
                self = OpenSlide(file)
                raise OpenslideObject("L'objet est un OpenSlide.")
            raise Unknown("Le type de fichier n'est pas ouvrable.")
        raise Unknown(
            "Aucune syntaxe n'a été reconnue."
            "Merci de lire la documentation avant de rééssayer."
        )
