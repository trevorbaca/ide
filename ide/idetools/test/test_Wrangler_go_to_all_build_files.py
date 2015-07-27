# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_all_build_files_01():
    r'''From scores to build depot.
    '''

    input_ = 'uu q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        ]
    assert abjad_ide._transcript.titles == titles