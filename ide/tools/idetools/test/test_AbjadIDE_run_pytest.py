# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_run_pytest_01():

    input_ = 'red~example~score pt q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert ' test session starts ' in contents
    assert 'collected 1 items' in contents
    assert 'test/test_import.py .' in contents
    assert ' 1 passed in ' in contents