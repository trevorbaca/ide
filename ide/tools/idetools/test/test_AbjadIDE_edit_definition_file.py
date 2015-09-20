# -*- coding: utf-8 -*-
from abjad import *
import ide


def test_AbjadIDE_edit_definition_file_01():
    r'''In material package.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm magic~numbers df q'
    abjad_ide._start_abjad_ide(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_edit_definition_file_02():
    r'''In segment package.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score gg A df q'
    abjad_ide._start_abjad_ide(input_=input_)

    assert abjad_ide._session._attempted_to_open_file