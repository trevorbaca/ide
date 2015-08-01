# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_make_file_01():

    path = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'test-file.txt',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score u new test-file.txt q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(path)