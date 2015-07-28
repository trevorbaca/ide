# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_PackageManager_edit_definition_py_01():
    r'''In material package.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers de q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_PackageManager_edit_definition_py_02():
    r'''In segment package.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g A de q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file