# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_invoke_shell_01():

    input_ = 'red~example~score mm tempo~inventory !pwd q'
    abjad_ide._start(input_=input_)

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_02():
    r'''Works at home.
    '''

    input_ = '!pwd q'
    abjad_ide._start(input_=input_)

    path = configuration.abjad_ide_example_scores_directory
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_03():
    r'''Works in build directory.
    '''

    input_ = 'red~example~score bb !pwd q'
    abjad_ide._start(input_=input_)

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents