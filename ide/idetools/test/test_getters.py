# -*- encoding: utf-8 -*-
from abjad import *
import ide
session = ide.idetools.Session()



def test_getters_01():

    getter = ide.idetools.getters.get_duration(
        'foo bar',
        session=session,
        )
    getter._session._pending_input = 'asdf (1, 16)'
    assert getter._run() == Duration(1, 16)


def test_getters_02():
    r'''Allows none.
    '''

    getter = ide.idetools.getters.get_duration(
        'foo bar',
        session=session,
        )
    getter._session._pending_input = 'None'
    assert getter._run() is None


def test_getters_03():

    getter = ide.idetools.getters.get_number(
        'foo bar',
        session=session,
        )
    getter._session._pending_input = '7'
    assert getter._run() == 7


def test_getters_04():

    getter = ide.idetools.getters.get_number(
        'foo bar',
        session=session,
        )
    getter._session._pending_input = '7.5'
    assert getter._run() == 7.5