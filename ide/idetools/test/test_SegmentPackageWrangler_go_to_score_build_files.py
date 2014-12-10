# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_score_build_files_01():
    r'''From segments directory to build directory.
    '''

    input_ = 'red~example~score g u q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - build directory',
        ]
    assert abjad_ide._transcript.titles == titles