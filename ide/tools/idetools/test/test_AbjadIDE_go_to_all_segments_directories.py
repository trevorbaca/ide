# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_segments_directories_01():
    r'''From scores to all segments directories.
    '''

    input_ = 'gg q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all segments directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles