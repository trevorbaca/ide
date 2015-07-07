# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_build_files_01():
    r'''From top level to all build files.
    '''

    input_ = 'hh uu q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        'Abjad IDE - build depot',
        ]
    assert abjad_ide._transcript.titles == titles