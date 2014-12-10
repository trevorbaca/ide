# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_pytest_01():
    r'''Works on all visible segment packages in library.
    '''

    input_ = 'gg pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_SegmentPackageWrangler_pytest_02():
    r'''Works on all segment packages in a score.
    '''

    input_ = 'red~example~score g pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_SegmentPackageWrangler_pytest_03():
    r'''Works on a single segment package.
    '''

    input_ = 'red~example~score g A pt q'
    abjad_ide._run(input_=input_)
    transcript_contents = abjad_ide._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents