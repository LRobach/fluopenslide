"""Setup script to install kill_openslide_fluo."""

from setuptools import setup, find_packages
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="kill_openslide_fluo",
    version="0.0.0",
    description="Opening fluorescence .czi files",
    author="Louison Robach",
    author_email="louison.robach@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "numpy",
        "aicspylibczi"
        "matplotlib"
        "pathlib"
        "xml"
        "aicsimageio"
    ],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
