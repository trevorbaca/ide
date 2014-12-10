# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_invoke_shell_01():
    r'''Outside of score package.
    '''

    input_ = 'yy !pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.score_manager_directory,
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents


def test_StylesheetWrangler_invoke_shell_02():
    r'''Inside score package.
    '''

    input_ = 'red~example~score y !pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents