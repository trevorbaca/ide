# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_pytest_01():
    r'''Works on all visible score packages.
    '''

    input_ = 'pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        '3 testable assets found ...',
        ]

    for string in strings:
        assert string in transcript_contents


def test_ScorePackageWrangler_pytest_02():
    r'''Works on a single score package.
    '''

    input_ = 'red~example~score pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        '1 testable asset found ...',
        ]

    for string in strings:
        assert string in transcript_contents