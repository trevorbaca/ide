# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_pytest_01():
    r'''Works on all test files in all maker file directories.
    '''

    input_ = 'kk pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'testable assets found',
        ]

    for string in strings:
        assert string in transcript_contents


def test_MakerFileWrangler_pytest_02():
    r'''Works on all test files in a single maker file directory.
    '''

    input_ = 'red~example~score k pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'testable assets found',
        ]

    for string in strings:
        assert string in transcript_contents