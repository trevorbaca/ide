# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_quit_01():
    r'''In material package.
    '''
    
    input_ = 'red~example~score mm tempo~inventory q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents


def test_AbjadIDE_quit_02():
    r'''In segment package.
    '''
    
    input_ = 'red~example~score gg A q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents

def test_AbjadIDE_quit_03():
    r'''In score package.
    '''

    input_ = 'red~example~score q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents