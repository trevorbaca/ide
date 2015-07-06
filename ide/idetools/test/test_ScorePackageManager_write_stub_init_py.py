# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_write_stub_init_py_01():

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        '__init__.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score ns y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(path)
        contents = abjad_ide._transcript.contents
        assert 'Will write stub to' in contents