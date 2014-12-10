# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    abjad_ide._configuration.example_score_packages_directory,
    'red_example_score',
    'segments',
    'segment_01',
    '__metadata__.py',
    )


def test_SegmentPackageManager_list_metadata_py_01():

    input_ = 'red~example~score g A mdl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert metadata_py_path in contents