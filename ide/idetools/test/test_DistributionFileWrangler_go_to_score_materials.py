# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_score_materials_01():
    r'''From distribution directory to materials directory.
    '''

    input_ = 'red~example~score d m q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Red Example Score (2013) - materials directory',
        ]
    assert abjad_ide._transcript.titles == titles