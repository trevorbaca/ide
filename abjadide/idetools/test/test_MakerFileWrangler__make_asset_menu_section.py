# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_MakerFileWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'blue~example~score k q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - makers directory',
        ]
    assert ide._transcript.titles == titles