# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_SegmentPackageManager_list_versions_directory_01():
    r'''Abjad IDE displays informative string when no versions
    directory exists and raises no exceptions.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g 1 vl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'definition_0001.py illustration_0001.ly illustration_0001.pdf'
    assert string in contents