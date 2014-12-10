# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_make_package_01():
    r'''Makes segment package.
    '''

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'versions',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score g new segment~04 y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(path)
        session = abjad_ide.idetools.Session(is_test=True)
        manager = abjad_ide.idetools.SegmentPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries