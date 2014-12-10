# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_PitchRange_autoedit_01():
    r'''Edits pitch range.
    '''

    session = ide.idetools.Session(is_test=True)
    target = pitchtools.PitchRange()
    autoeditor = ide.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = '1 [F#3, C5) q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == pitchtools.PitchRange('[F#3, C5)')

    session = ide.idetools.Session(is_test=True)
    target = pitchtools.PitchRange()
    autoeditor = ide.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = '1 (A0, C8] q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == pitchtools.PitchRange('(A0, C8]')