from importlib.metadata import version

import isrtools
from isrtools._version import __version__


def test_package_imports():
    assert isrtools.__name__ == "isrtools"


def test_version_matches_installed_metadata():
    assert __version__ == version("isrtools")
