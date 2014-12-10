# -*- encoding: utf-8 -*-
from abjad import *
import ide
ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_pytest_01():

    input_ = 'red~example~score pt q'
    ide._run(input_=input_)
    transcript_contents = ide._transcript.contents

    strings = [
        'Running py.test ...',
        '1 testable asset found ...',
        ]

    for string in strings:
        assert string in transcript_contents