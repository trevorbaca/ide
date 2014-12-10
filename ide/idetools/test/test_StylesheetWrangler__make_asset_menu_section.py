# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_StylesheetWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'blue~example~score y q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - stylesheets directory',
        ]
    assert abjad_ide._transcript.titles == titles