# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'uu dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        'No testable assets found.',
        ]
    for string in strings:
        assert string in contents

    
def test_BuildFileWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score u dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        'No testable assets found.',
        ]
    for string in strings:
        assert string in contents