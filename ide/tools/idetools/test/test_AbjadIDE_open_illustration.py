# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_open_illustration_01():
    r'''In material package.
    '''

    input_ = 'red~example~score m magic~numbers o q'
    abjad_ide._run_main_menu(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_illustration_02():
    r'''In segment package.
    '''

    input_ = 'red~example~score g A o q'
    abjad_ide._run_main_menu(input_=input_)

    assert abjad_ide._session._attempted_to_open_file