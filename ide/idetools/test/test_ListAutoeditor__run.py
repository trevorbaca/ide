# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ListAutoeditor__run_01():
    r'''Edits built-in list.
    '''

    session = ide.idetools.Session(is_test=True)
    autoeditor = ide.idetools.ListAutoeditor(session=session)
    input_ = "17 99 'foo' done q"
    autoeditor._session._is_autoadding = True
    autoeditor._session._pending_input = input_
    autoeditor._run()
    contents = autoeditor._transcript.contents

    assert autoeditor.target == [17, 99, 'foo']
    assert 'List (EDIT)' in contents


def test_ListAutoeditor__run_02():
    r'''Edits empty tempo inventory.

    Works with pairs.
    '''

    session = ide.idetools.Session(is_test=True)
    target = indicatortools.TempoInventory()
    autoeditor = ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add ((1, 4), 60)'
    input_ +=  ' add (Duration(1, 4), 72)'
    input_ += ' add ((1, 4), 84) done'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60),
        Tempo(Duration(1, 4), 72),
        Tempo(Duration(1, 4), 84),
        ])
    assert autoeditor.target == inventory


def test_ListAutoeditor__run_03():
    r'''Edits empty pitch range inventory.
    '''

    session = ide.idetools.Session(is_test=True)
    target = pitchtools.PitchRangeInventory()
    autoeditor = ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add [C0, C6]'
    input_ += ' add [C1, C7]'
    input_ += ' add [C2, C8]'
    input_ += ' rm 1 mv 1 2 q'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    assert autoeditor.target == pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, C8]'),
        pitchtools.PitchRange('[C1, C7]'),
        ])


def test_ListAutoeditor__run_04():
    r'''Edits empty octave transposition mapping.
    '''

    session = ide.idetools.Session(is_test=True)
    target = pitchtools.Registration()
    autoeditor = ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = "add ('[A0, F#4]', 22)"
    input_ += " add ('(F#4, C8]', 26) done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    mapping = pitchtools.Registration([
        ('[A0, F#4]', 22),
        ('(F#4, C8]', 26),
        ])
    assert autoeditor.target == mapping


def test_ListAutoeditor__run_05():
    r'''Edits empty octave transposition mapping.
    '''

    session = ide.idetools.Session(is_test=True)
    target = pitchtools.Registration()
    autoeditor = ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = "add ('[A0, F#4]', 22)"
    input_ +=  " add ('(F#4, C8]', 26) done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    mapping = pitchtools.Registration(
            [('[A0, F#4]', 22), ('(F#4, C8]', 26)],
            )

    assert autoeditor.target == mapping


def test_ListAutoeditor__run_06():
    r'''Edits instrument inventory.
    '''

    session = ide.idetools.Session(is_test=True)
    target = instrumenttools.InstrumentInventory()
    autoeditor = ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add flute add piccolo done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Piccolo(),
        ])

    assert autoeditor.target == inventory


def test_ListAutoeditor__run_07():
    r'''Edits view.
    '''

    session = ide.idetools.Session(is_test=True)
    target = ide.idetools.View()
    autoeditor = ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add first~pattern add second~pattern done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    view = ide.idetools.View([
        'first pattern',
        'second pattern',
        ])

    assert autoeditor.target == view


def test_ListAutoeditor__run_08():

    input_ = 'red~example~score m performer~inventory da q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - performer inventory',
        'Red Example Score (2013) - materials directory - performer inventory (EDIT)',
        ]
    assert abjad_ide._transcript.titles == titles