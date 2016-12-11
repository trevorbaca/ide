# -*- coding: utf-8 -*-
import abjad
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_aliases_file_01():

    input_ = 'red~example~score mm tempo~inventory als q'
    abjad_ide._start(input_=input_)
    
    assert abjad_ide._session._attempted_to_open_file