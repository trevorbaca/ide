# -*- encoding: utf-8 -*-
from abjad import *
import ide
session = ide.idetools.Session(is_test=True)


def test_Selector__run_01():

    items=['apple', 'banana', 'cherry']
    selector = ide.idetools.Selector(
        items=items,
        session=session,
        )
    selector._session._is_test = True

    selector._session._pending_input = 'apple'
    assert selector._run() == 'apple'

    selector._session._pending_input = 'banana'
    assert selector._run() == 'banana'

    selector._session._pending_input = 'cherry'
    assert selector._run() == 'cherry'