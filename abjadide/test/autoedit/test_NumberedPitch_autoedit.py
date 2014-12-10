# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_NumberedPitch_autoedit_01():
    r'''Changes pitch number to another integer.
    '''

    session = abjadide.idetools.Session(is_test=True)
    target = pitchtools.NumberedPitch(13)
    autoeditor = abjadide.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'pn 14 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    assert autoeditor.target == pitchtools.NumberedPitch(14)


def test_NumberedPitch_autoedit_02():
    r'''Changes pitch number to float.
    '''

    session = abjadide.idetools.Session(is_test=True)
    target = pitchtools.NumberedPitch(13)
    autoeditor = abjadide.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'pn 13.5 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    assert autoeditor.target == pitchtools.NumberedPitch(13.5)