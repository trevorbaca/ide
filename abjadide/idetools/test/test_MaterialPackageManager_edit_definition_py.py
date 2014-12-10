# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_MaterialPackageManager_edit_definition_py_01():

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers de q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file