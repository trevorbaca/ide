# -*- coding: utf-8 -*-
import abjad
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_ly_01():

    input_ = 'red~example~score gg A ly q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file