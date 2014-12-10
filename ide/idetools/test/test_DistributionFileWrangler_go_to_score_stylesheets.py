# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_score_stylesheets_01():
    r'''Goes from distribution directory to stylesheets directory.
    '''

    input_ = 'red~example~score d y q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Red Example Score (2013) - stylesheets directory',
        ]
    assert abjad_ide._transcript.titles == titles