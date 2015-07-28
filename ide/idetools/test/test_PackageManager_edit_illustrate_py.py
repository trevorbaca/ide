# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_PackageManager_edit_illustrate_py_01():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers le q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file