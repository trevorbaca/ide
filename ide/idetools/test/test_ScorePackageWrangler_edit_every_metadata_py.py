# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_edit_every_metadata_py_01():

    input_ = 'mde* y q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file