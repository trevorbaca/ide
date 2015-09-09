# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE__get_repository_root_directory_01():

    score_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        )

    repository_root_directory = abjad_ide._get_repository_root_directory(
        score_path,
        )
    assert repository_root_directory == configuration.abjad_ide_root_directory