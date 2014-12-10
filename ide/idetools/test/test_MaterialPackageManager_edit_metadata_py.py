# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_edit_metadata_py_01():

    input_ = 'red~example~score m magic~numbers mde q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file