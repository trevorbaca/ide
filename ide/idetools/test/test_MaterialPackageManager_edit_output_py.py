# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_edit_output_py_01():

    input_ = 'red~example~score m magic~numbers oe q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file