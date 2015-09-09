# -*- coding: utf-8 -*-
from abjad import *
import ide


def test_Session___repr___01():

    session = ide.tools.idetools.Session(input_='foo')
    string = "Session(input_='foo')"
    assert repr(session) == string