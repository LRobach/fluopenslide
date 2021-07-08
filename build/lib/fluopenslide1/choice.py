from fluopenslide import FluOpenSlide
from openslide import OpenSlide
import os
from os.path import basename
import matplotlib.pyplot as plt


L = [
    '.mrxs', '.svs', '.tif', '.ndpi', '.vms', '.vmu',
    '.scn', '.tiff', '.svslide', '.bif'
]


class Unknown(Exception):
    """
    The object can not be opened.
    """
    pass


class choice(FluOpenSlide, OpenSlide):
    """
    Decide which program use between OpenSlide and FluOpenSlide.

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
        self._filename, self.extension = os.path.splitext(file)

        if (choice == "FluOpenSlide" or choice == "fluopenslide"):
            FluOpenSlide.__init__(self, file)
            self = FluOpenSlide(file)
            print(
                'Le fichier est à présent un objet FluOpenSlide.'
            )
            return(None)
        if (choice == "Openslide" or choice == "openslide"):
            OpenSlide.__init__(self, file)
            self = Openslide(file)
            print(
                'Le fichier est à présent un objet OpenSlide.'
            )
            return(None)
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
                print("L'objet est un FluOpenSlide.")
                return(None)
            if (self.extension in L):
                OpenSlide.__init__(self, file)
                self = OpenSlide(file)
                print("L'objet est un OpenSlide.")
                return(None)
            raise Unknown("Le type de fichier n'est pas ouvrable.")
        raise Unknown(
            "Aucune syntaxe n'a été reconnue."
            "Merci de lire la documentation avant de rééssayer."
        )
