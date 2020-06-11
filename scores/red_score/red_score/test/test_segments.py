import os
import pathlib
import sys

import pytest

import abjad
import ide

abjad_ide = ide.AbjadIDE()
scores = pathlib.Path(*pathlib.Path(__file__).parts[:-4])
path = abjad.Path(__file__, scores=scores)
directories = path.segments.list_paths()


@pytest.mark.parametrize("directory", directories)
def test_segments_01(directory):
    exit_code = abjad_ide.check_definition_py(directory)
    if exit_code != 0:
        sys.exit(exit_code)


@pytest.mark.parametrize("directory", directories)
def test_segments_02(directory):
    # only run on Travis because segment illustration usually takes a while
    if not os.getenv("TRAVIS"):
        return
    exit_code = abjad_ide.make_illustration_pdf(directory)
    if exit_code != 0:
        sys.exit(exit_code)
