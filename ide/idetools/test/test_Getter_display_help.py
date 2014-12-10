# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_Getter_display_help_01():
    r'''Question mark displays help.
    '''

    input_ = 'red~example~score m new ? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string  = 'Value must be string.'
    assert string in contents


def test_Getter_display_help_02():
    r'''Help string displays help.
    '''

    input_ = 'red~example~score m new help q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'Value must be string.'
    assert string in contents