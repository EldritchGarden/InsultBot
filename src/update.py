"""
Downloads wordlists in csv format from a given Gist
"""

import shutil
import os
import requests
import logging

log = logging.getLogger(__name__)
BASEPATH = os.path.dirname(__file__)

def download_file(url: str, destination: str):
    """Downloads a file from the url to the destination"""

    with requests.get(url, stream=True) as r:
        with open(destination, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def wordlists(url: str, files: list):
    """Downloads wordlists from a gist
    url    - base url for the raw files, without the filename
    files  - list of filenames to get from the gist
    """

    wordlists_path = f'{BASEPATH}/Wordlists'

    if not os.path.exists(wordlists_path):
        os.makedirs(wordlists_path)

    for fname in files:
        furl = f'{url}/{fname}'
        fpath = f'{wordlists_path}/{fname}'

        download_file(furl, fpath)
