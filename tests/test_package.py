from __future__ import annotations

import importlib.metadata

import isrtools as m


def test_version() -> None:
    assert importlib.metadata.version("isrtools") == m.__version__
