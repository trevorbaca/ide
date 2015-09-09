# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_distribution_directories_01():
    r'''From scores to all distribution directories.
    '''

    input_ = 'dd q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all distribution directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles