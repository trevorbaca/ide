# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_score_segments_directory_01():
    r'''Goes from build directory to segments directory.
    '''

    input_ = 'red~example~score u g q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - segments directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles