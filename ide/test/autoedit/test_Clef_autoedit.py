# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Clef_autoedit_01():
    r'''Edits clef name.
    '''

    target = Clef('alto')
    session = ide.idetools.Session(is_test=True)
    autoeditor = ide.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm tenor done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Clef('tenor')