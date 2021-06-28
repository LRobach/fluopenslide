from killopenslide import KillOpenSlide
from openslide import OpenSlide
import os
from os.path import basename


L = [
    '.mrxs', '.svs', '.tif', '.ndpi', '.vms', '.vmu',
    '.scn', '.tiff', '.svslide', '.bif'
]


class OpenslideObject(Exception):
    """
    The object created can be opened with OpenSlide.
    """
    pass


class KillOpenSlideObject(Exception):
    """
    The object created can be opened with KillOpenSlide.
    """
    pass


class Unknown(Exception):
    """
    The object can not be opened.
    """
    pass


class choice(KillOpenSlide, OpenSlide):
    """
    Decide witch program use between OpenSlide and KillOpenSlide.

    """
    def __init__(self, file, choice=None):
        """
        Parameters
        ---------
        file : str
           The path to your czi file.
        choice : str
            Have to be "KillOpenSlide" or "Openslide".
            If there is no choice, focus on the file extension.
        """
        self.name, self.extension = os.path.splitext(file)

        if (choice == "KillOpenSlide" or choice == "killopenslide"):
            KillOpenSlide.__init__(self, file)
            self = KillOpenSlide(file)
            raise KillOpenSlideObject(
                'Le fichier est à présent un objet KillOpenSlide.'
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
                KillOpenSlide.__init__(self, file)
                self = KillOpenSlide(file)
                raise KillOpenSlideObject("L'objet est un KillOpenSlide.")
            if (self.extension in L):
                OpenSlide.__init__(self, file)
                self = OpenSlide(file)
                raise OpenslideObject("L'objet est un OpenSlide.")
            raise Unknown("Le type de fichier n'est pas ouvrable.")
        raise Unknown(
            "Aucune syntaxe n'a été reconnue."
            "Merci de lire la documentation avant de rééssayer."
        )
