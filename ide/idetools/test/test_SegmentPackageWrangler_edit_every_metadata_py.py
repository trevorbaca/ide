# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_edit_every_metadata_py_01():

    input_ = 'red~example~score g mde* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert abjad_ide._session._attempted_to_open_file

    package_names = (
        'segment_01',
        'segment_02',
        'segment_03',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            abjad_ide._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            package_name,
            '__metadata__.py',
            )

    lines = []
    lines.append('Will open ...')
    lines.extend(paths)

    for line in lines:
        assert line in contents