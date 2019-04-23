import os

import pytest

import pygraphutils.util.file as f
from pathlib import Path
import shutil

FILENAME = "/aaa/bbb/ccc/ddd.ee"


@pytest.fixture
def base_dir():
    return "tmp/test"


@pytest.fixture
def test_dirs(base_dir):
    test_dirs = []
    for i in range(0, 10):
        d = "%s/dir%d" % (base_dir, i)
        f.mkdir(d)
        test_dirs.append(d)

    yield test_dirs

    shutil.rmtree(base_dir)


@pytest.fixture
def base_dir2():
    return "tmp/test2"


@pytest.fixture
def test_files(base_dir2):
    test_files = []
    f.mkdir(base_dir2)
    for i in range(0, 10):
        filename = "%s/f%d.ext%d" % (base_dir2, i, i % 2)
        Path(filename).touch()
        test_files.append(filename)

    yield test_files

    shutil.rmtree(base_dir2)


def test_basename():
    assert f.basename(FILENAME) == "ddd"


def test_ext():
    assert f.ext(FILENAME) == "ee"


def test_get_filenames(base_dir, test_dirs):
    assert f.get_filenames(base_dir, "") == test_dirs


def test_get_filenames2(base_dir2, test_files):
    assert f.get_filenames(base_dir2, "ext1") == [
        f for f in test_files if f.endswith(".ext1")
    ]


def test_mkdir(base_dir):
    assert f.mkdir(base_dir)
    assert not f.mkdir(base_dir)
    assert not f.mkdir(base_dir)
