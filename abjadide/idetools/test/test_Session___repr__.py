# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_Session___repr___01():

    session = abjadide.idetools.Session(input_='foo')
    string = "Session(initial_input_='foo',"
    string += " input_='foo')"
    assert repr(session) == string