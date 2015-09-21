# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_lilypond_log_01():

    input_ = 'red~example~score mm tempo~inventory log q'
    abjad_ide._run_main_menu(input_=input_)
    
    assert abjad_ide._session._attempted_to_open_file