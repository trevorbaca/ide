# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_remove_files_01():

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'foo-file.txt',
        )

    with systemtools.FilesystemState(remove=[path]):
        with open(path, 'w') as file_pointer:
            file_pointer.write('This is a test file.')
        assert os.path.exists(path)
        input_ = 'red~example~score d rm foo-file.txt remove q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(path)