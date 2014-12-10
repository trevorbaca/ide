# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide


def test_ScorePackageManager_doctest_01():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        '67 testable assets found ...',
        '\n__init__.py OK\n',
        '\n__metadata__.py OK\n',
        '\nmakers/RedExampleScoreTemplate.py OK\n',
        '0 of 0 tests passed in 67 modules.',
        ]

    for string in strings:
        assert string in contents