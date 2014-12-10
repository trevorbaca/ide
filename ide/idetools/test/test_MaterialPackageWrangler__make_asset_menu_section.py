# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    input_ = 'blue~example~score m q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - materials directory',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MaterialPackageWrangler__make_asset_menu_section_02():
    r'''Omits score annotation inside score.
    '''

    input_ = 'red~example~score m q'
    abjad_ide._run(input_=input_)
    assert '(Red Example Score)' not in abjad_ide._transcript.contents


def test_MaterialPackageWrangler__make_asset_menu_section_03():
    r'''Includes score annotation outside of score.
    '''

    input_ = 'mm q'
    abjad_ide._run(input_=input_)
    assert 'Red Example Score:' in abjad_ide._transcript.contents