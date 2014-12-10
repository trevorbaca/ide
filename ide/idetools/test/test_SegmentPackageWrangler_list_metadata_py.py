# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_list_metadata_py_01():

    metadata_py_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        '__metadata__.py',
        )

    input_ = 'red~example~score g mdl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert metadata_py_path in contents


def test_SegmentPackageWrangler_list_metadata_py_02():

    input_ = 'gg mdl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert abjad_ide._configuration.wrangler_views_metadata_file in contents