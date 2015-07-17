# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_write_stub_definition_py_01():

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score g A ds y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(path)
        assert not filecmp.cmp(path, path + '.backup')