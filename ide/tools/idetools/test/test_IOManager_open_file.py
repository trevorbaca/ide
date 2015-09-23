# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_IOManager_open_file_01():
    r'''@-addressing to distribution file.
    '''

    input_ = 'red~example~score @program-notes.txt q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_02():
    r'''@-addressing to etc file.
    '''

    input_ = 'red~example~score @notes.txt q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_03():
    r'''@-addressing to makers file.
    '''

    input_ = 'red~example~score @RM q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_04():
    r'''@-addressing to makers file with line number
    '''

    input_ = 'red~example~score @RM+14 q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_05():
    r'''@-addressing to stylesheet.
    '''

    input_ = 'red~example~score @gasso q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles