# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_run_doctest_01():
    r'''In score directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~example~score dt q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    # control characters format blue text
    assert '__metadata__.py \x1b[94mOK\x1b[0m' in contents
    assert 'build/__metadata__.py \x1b[94mOK\x1b[0m' in contents
    assert 'build/__views__.py \x1b[94mOK\x1b[0m' in contents
    assert 'makers/ScoreTemplate.py \x1b[94mOK\x1b[0m' in contents
    assert '4 of 4 tests pass in 33 modules.'


def test_AbjadIDE_run_doctest_02():
    r'''In makers directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~example~score kk dt q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    # control characters format blue text
    assert '__metadata__.py \x1b[94mOK\x1b[0m' in contents
    assert 'build/__metadata__.py \x1b[94mOK\x1b[0m' in contents
    assert 'build/__views__.py \x1b[94mOK\x1b[0m' in contents
    assert 'makers/ScoreTemplate.py \x1b[94mOK\x1b[0m' in contents
    assert '4 of 4 tests pass in 33 modules.'