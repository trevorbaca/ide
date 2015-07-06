# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    abjad_ide._configuration.example_score_packages_directory,
    'red_example_score',
    'red_example_score',
    '__metadata__.py',
    )


def test_ScorePackageManager_list_metadata_py_01():

    input_ = 'red~example~score mdl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert metadata_py_path in contents