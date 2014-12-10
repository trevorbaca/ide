# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Session_command_history_string_01():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._allow_unknown_command_during_test = True
    input_ = 'foo bar blah q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session.command_history_string == input_