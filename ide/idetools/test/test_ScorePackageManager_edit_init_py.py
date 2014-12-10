# -*- encoding: utf-8 -*-
from abjad import *
import ide
ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_init_py_01():

    input_ = 'red~example~score ne q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file