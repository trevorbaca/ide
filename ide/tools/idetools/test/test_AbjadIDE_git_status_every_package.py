# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_git_status_every_package_01():
    r'''Works with all scores.
    '''

    input_ = 'st* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_AbjadIDE_git_status_every_package_02():
    r'''Make sure command is not available in incorrect directories.
    '''

    input_ = 'red~example~score st* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert "Unknown command: 'st*'." in contents