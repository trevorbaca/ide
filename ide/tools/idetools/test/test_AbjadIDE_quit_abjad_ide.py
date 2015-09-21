# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_quit_abjad_ide_01():
    
    input_ = 'q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents


def test_AbjadIDE_quit_abjad_ide_02():
    
    input_ = 'red~example~score bb q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents