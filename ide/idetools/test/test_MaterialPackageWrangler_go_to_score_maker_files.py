# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_score_maker_files_01():
    r'''From materials directory to makers directory.
    '''

    input_ = 'red~example~score m k q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._transcript.titles == titles