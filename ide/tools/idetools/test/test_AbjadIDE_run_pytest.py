# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_run_pytest_01():

    input_ = 'red~example~score pt q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Running pytest on' in contents
    assert abjad_ide._io_manager._session._attempted_method == '_run_pytest'
