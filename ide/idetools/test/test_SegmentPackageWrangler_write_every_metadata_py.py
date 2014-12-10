# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_write_every_metadata_py_01():

    package_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            abjad_ide._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            package_name,
            '__metadata__.py',
            )
        paths.append(path)

    with systemtools.FilesystemState(keep=paths):
        input_ = 'red~example~score g mdw* y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents

    assert 'Will write ...' in contents
    for path in paths:
        assert path in contents
    assert '3 __metadata__.py files rewritten.' in contents


def test_SegmentPackageWrangler_write_every_metadata_py_02():

    input_ = 'gg mdw* n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Will write ...' in contents
    assert '__metadata__.py' in contents