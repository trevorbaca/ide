# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    abjad_ide._configuration.example_score_packages_directory,
    'red_example_score',
    'red_example_score',
    'segments',
    'segment_01',
    '__metadata__.py',
    )


def test_SegmentPackageManager_write_metadata_py_01():

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'red~example~score g A mdw q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents