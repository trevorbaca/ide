# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_AbjadIDE__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'blue~example~score g segment~01 q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments directory',
        'Blue Example Score (2013) - segments directory - segment 01',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles