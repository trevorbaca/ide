# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_ScorePackageManager_doctest_01():

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score dt q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

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