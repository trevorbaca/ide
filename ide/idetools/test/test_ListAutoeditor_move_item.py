# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ListAutoeditor_move_item_01():
    r'''Doesn't blow up when (b) is entered during move.
    '''

    session = abjad_ide.idetools.Session(is_test=True)
    target = [17, 99, 'foo']
    autoeditor = abjad_ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'mv 1 b q'
    autoeditor._session._pending_input = input_
    autoeditor._run()


def test_ListAutoeditor_move_item_02():
    r'''Large numbers like 99 can be used as move-to number.
    '''

    session = abjad_ide.idetools.Session(is_test=True)
    target = [17, 99, 'foo']
    autoeditor = abjad_ide.idetools.ListAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'mv 1 99 q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == [99, 'foo', 17]