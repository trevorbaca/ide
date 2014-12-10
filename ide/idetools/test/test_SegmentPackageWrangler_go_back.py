# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_back_01():

    input_ = 'red~example~score g b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_back_02():

    input_ = 'gg b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments depot',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles