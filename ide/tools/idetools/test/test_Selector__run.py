# -*- encoding: utf-8 -*-
from abjad import *
import ide
session = ide.tools.idetools.Session(is_test=True)
io_manager = ide.tools.idetools.IOManager(session=session)


def test_Selector__run_01():

    items=['apple', 'banana', 'cherry']
    selector = ide.tools.idetools.Selector(items=items)
    io_manager._session._is_test = True

    io_manager._session._pending_input = 'apple'
    assert selector._run(io_manager=io_manager) == 'apple'

    io_manager._session._pending_input = 'banana'
    assert selector._run(io_manager=io_manager) == 'banana'

    io_manager._session._pending_input = 'cherry'
    assert selector._run(io_manager=io_manager) == 'cherry'