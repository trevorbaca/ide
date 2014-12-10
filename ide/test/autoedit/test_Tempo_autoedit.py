# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide


def test_Tempo_autoedit_01():
    r'''Creates default tempo.
    '''

    target = Tempo()
    session = abjad_ide.idetools.Session(is_test=True)
    autoeditor = abjad_ide.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target is target


def test_Tempo_autoedit_02():
    r'''Edits tempo duration with pair.
    '''

    session = abjad_ide.idetools.Session(is_test=True)
    autoeditor = abjad_ide.idetools.Autoeditor(
        session=session,
        target=Tempo(),
        )
    input_ = 'Duration (1, 8) units 98 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Tempo(Duration(1, 8), 98)


def test_Tempo_autoedit_03():
    r'''Edits tempo duration with duration object.
    '''

    session = abjad_ide.idetools.Session(is_test=True)
    autoeditor = abjad_ide.idetools.Autoeditor(
        session=session,
        target=Tempo(),
        )
    input_ = 'Duration Duration(1, 8) units 98 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Tempo(Duration(1, 8), 98)

