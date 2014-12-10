# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_invoke_shell_01():

    input_ = 'red~example~score g A !pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents