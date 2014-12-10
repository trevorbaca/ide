# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Session___repr___01():

    session = ide.idetools.Session(input_='foo')
    string = "Session(initial_input_='foo',"
    string += " input_='foo')"
    assert repr(session) == string