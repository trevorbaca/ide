# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Getter__run_01():
    r'''Entering junk during confirmation displays value reminder message.
    '''

    input_ = 'red~example~score u mc foo n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = "Value for 'ok?' must be 'y' or 'n'."
    assert string in contents


def test_Getter__run_02():
    r'''Entering 'n' during confirmation cancels getter.
    '''

    input_ = 'red~example~score u mc n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Value for' not in contents


def test_Getter__run_03():
    r'''Entering 'N' during confirmation cancels getter.
    '''

    input_ = 'red~example~score u mc N q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Value for' not in contents