# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_all_distribution_files_01():
    r'''From scores to distribution depot.
    '''

    input_ = 'dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles