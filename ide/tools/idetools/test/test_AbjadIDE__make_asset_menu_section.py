# -*- coding: utf-8 -*-
from abjad import *
import ide
configuration = ide.tools.idetools.AbjadIDEConfiguration()
session = ide.tools.idetools.Session()
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


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


def test_AbjadIDE__make_asset_menu_section_02():
    r'''Omits score annotation when listing segments in score.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Red Example Score (2013) - segments'
    assert string in contents
    assert 'A\n' in contents


def test_AbjadIDE__make_asset_menu_section_03():
    r'''Behaves gracefully when no materials are found.
    '''

    input_ = 'blue~example~score m q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - materials directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE__make_asset_menu_section_04():
    r'''Omits score annotation inside score.
    '''

    input_ = 'red~example~score m q'
    abjad_ide._run_main_menu(input_=input_)
    assert '(Red Example Score)' not in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE__make_asset_menu_section_05():
    r'''Includes score annotation outside of score.
    '''

    input_ = 'mm q'
    abjad_ide._run_main_menu(input_=input_)
    assert 'Red Example Score:' in abjad_ide._io_manager._transcript.contents