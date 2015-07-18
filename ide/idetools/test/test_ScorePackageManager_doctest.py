# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_ScorePackageManager_doctest_01():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        '46 testable assets found ...',
        '\n__init__.py OK\n',
        '\n__metadata__.py OK\n',
        '\nmakers/RedExampleScoreTemplate.py OK\n',
        '0 of 0 tests passed in 46 modules.',
        ]

    for string in strings:
        assert string in contents