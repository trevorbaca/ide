# -*- encoding: utf-8 -*-
from abjad import *
import ide
configuration = ide.tools.idetools.Configuration()
session = ide.tools.idetools.Session()
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler__make_asset_menu_section_01():
    r'''Omits score annotation when listing segments in score.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'Red Example Score (2013) - segments'
    assert string in contents
    assert 'A\n' in contents


def test_Wrangler__make_asset_menu_section_02():
    r'''Behaves gracefully when no materials are found.
    '''

    input_ = 'blue~example~score m q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - materials directory',
        ]
    assert abjad_ide._transcript.titles == titles


def test_Wrangler__make_asset_menu_section_03():
    r'''Omits score annotation inside score.
    '''

    input_ = 'red~example~score m q'
    abjad_ide._run(input_=input_)
    assert '(Red Example Score)' not in abjad_ide._transcript.contents


def test_Wrangler__make_asset_menu_section_04():
    r'''Includes score annotation outside of score.
    '''

    input_ = 'mm q'
    abjad_ide._run(input_=input_)
    assert 'Red Example Score:' in abjad_ide._transcript.contents