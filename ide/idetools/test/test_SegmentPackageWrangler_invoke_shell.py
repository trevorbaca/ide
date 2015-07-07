# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_invoke_shell_01():
    r'''Outside of score package.
    '''

    input_ = 'gg !pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.abjad_ide_directory,
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents


def test_SegmentPackageWrangler_invoke_shell_02():
    r'''Inside score package.
    '''

    input_ = 'red~example~score g !pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents