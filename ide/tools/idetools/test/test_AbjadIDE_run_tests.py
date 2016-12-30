# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_run_tests_01():

    input_ = 'red~example~score tests q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Running doctest on' in contents
    assert '4 passed, 0 failed out of 4 tests in 46 modules.' in contents

    assert 'Running pytest on' in contents
    assert ' test session starts ' in contents
    assert 'collected 1 items' in contents
    assert 'test/test_import.py .' in contents
    assert ' 1 passed in ' in contents
