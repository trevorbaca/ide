# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_output_definition_py_01():

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        'output.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score m magic~numbers dp y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(path)
        contents = abjad_ide._transcript.contents
        assert 'Will write output material to' in contents