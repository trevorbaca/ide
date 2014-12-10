# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_list_every_metadata_py_01():

    input_ = 'mdl* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    path = abjad_ide._configuration.example_score_packages_directory
    paths = [
        os.path.join(path, 'blue_example_score'),
        os.path.join(path, 'etude_example_score'),
        os.path.join(path, 'red_example_score'),
        ]
    for path in paths:
        assert path in contents

    assert '__metadata__.py files found.' in contents