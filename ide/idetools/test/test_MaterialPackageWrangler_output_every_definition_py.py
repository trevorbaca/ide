# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_output_every_definition_py_01():

    input_ = 'red~example~score m dp* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    package_names = [
        'magic_numbers',
        'performer_inventory',
        'pitch_range_inventory',
        'tempo_inventory',
        'time_signatures',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            abjad_ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            'definition.py',
            )
        paths.append(path)

    assert 'Will output ...' in contents
    for path in paths:
        assert path in contents