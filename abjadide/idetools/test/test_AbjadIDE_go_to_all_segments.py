# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_segments_01():
    r'''From top level to all segments.
    '''

    input_ = 'hh gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles