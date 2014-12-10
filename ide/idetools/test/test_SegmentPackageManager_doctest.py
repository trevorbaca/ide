# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_SegmentPackageManager_doctest_01():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g A dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        '2 testable assets found ...',
        '0 of 0 tests passed in 2 modules.',
        ]