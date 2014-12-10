# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_edit_every_init_py_01():

    input_ = 'ne* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Will open ...' in contents

    package_names = (
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            abjad_ide._configuration.example_score_packages_directory,
            package_name,
            '__init__.py',
            )

    for path in paths:
        assert path in contents

    assert abjad_ide._session._attempted_to_open_file