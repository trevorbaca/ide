# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_pytest_01():
    r'''Works on all distribution files in library.
    '''

    input_ = 'dd pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_DistributionFileWrangler_pytest_02():
    r'''Works on all files in a single distribution directory.
    '''

    input_ = 'red~example~score d pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents