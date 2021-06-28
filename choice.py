from link_with_openslide import KillOpenSlide
from openslide import OpenSlide
import os
from os.path import basename
import matplotlib.pyplot as plt


L = [
    '.mrxs', '.svs', '.tif', '.ndpi', '.vms', '.vmu',
    '.scn', '.tiff', '.svslide', '.bif'
]


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
            print(
                'Le fichier est à présent un objet KillOpenSlide.'
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
                KillOpenSlide.__init__(self, file)
                self = KillOpenSlide(file)
                print("L'objet est un KillOpenSlide.")
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
