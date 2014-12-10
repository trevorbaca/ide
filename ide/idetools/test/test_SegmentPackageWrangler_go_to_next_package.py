# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide


def test_SegmentPackageWrangler_go_to_next_package_01():
    r'''Previous material package.
    '''

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g > > > > q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - segments directory - B',
        'Red Example Score (2013) - segments directory - C',
        'Red Example Score (2013) - segments directory - A',
        ]
    assert abjad_ide._transcript.titles == titles