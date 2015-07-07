# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_doctest_01():

    input_ = 'red~example~score m tempo~inventory dt q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        'Running doctest ...',
        '4 testable assets found ...',
        '0 of 0 tests passed in 4 modules.',
        ]
    for string in strings:
       assert string in contents