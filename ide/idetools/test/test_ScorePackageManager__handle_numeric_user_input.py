# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager__handle_numeric_user_input_01():

    input_ = 'red~example~score __init__.py q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_ScorePackageManager__handle_numeric_user_input_02():

    input_ = 'red~example~score 7 q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    strings = [
        '__init__.py',
        '__metadata__.py',
        '__views__.py',
        'segment_01',
        'segment_02',
        'segment_03',
        ]

    for string in strings:
        assert string in contents