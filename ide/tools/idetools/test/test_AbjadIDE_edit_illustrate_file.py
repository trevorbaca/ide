# -*- coding: utf-8 -*-
from abjad import *
import ide


def test_AbjadIDE_edit_illustrate_file_01():

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm magic~numbers ill q'
    abjad_ide._run_main_menu(input_=input_)

    assert abjad_ide._session._attempted_to_open_file