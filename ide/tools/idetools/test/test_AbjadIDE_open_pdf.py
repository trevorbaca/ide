# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    input_ = 'red~example~score mm magic~numbers pdf q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    input_ = 'red~example~score gg A pdf q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    input_ = 'blue~example~score gg segment~01 pdf q'
    abjad_ide._start(input_=input_)

    assert not abjad_ide._session._attempted_to_open_file
    contents = abjad_ide._io_manager._transcript.contents
    assert 'File does not exist:' in contents