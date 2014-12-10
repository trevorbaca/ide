# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_edit_every_init_py_01():

    input_ = 'red~example~score m ne* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    package_names = (
        'magic_numbers',
        'performer_inventory',
        'pitch_range_inventory',
        'tempo_inventory',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            abjad_ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            '__init__.py',
            )

    lines = []
    lines.append('Will open ...')
    lines.extend(paths)

    for line in lines:
        assert line in contents

    assert abjad_ide._session._attempted_to_open_file