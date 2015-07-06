# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'gg dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        'testable assets found ...',
        'tests passed in',
        ]
    for string in strings:
        assert string in contents

    
def test_SegmentPackageWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score g dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        '9 testable assets found ...',
        '0 of 0 tests passed in 9 modules.',
        ]
    for string in strings:
        assert string in contents