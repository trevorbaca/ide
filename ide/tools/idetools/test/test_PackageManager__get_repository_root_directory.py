# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager__get_repository_root_directory_01():

    score_path = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        )
    manager = ide.tools.idetools.PackageManager(
        path=score_path,
        session=abjad_ide._session,
        )

    repository_root_directory = manager._get_repository_root_directory()
    abjad_ide_root_directory = \
        manager._session._configuration.abjad_ide_root_directory
    assert repository_root_directory == abjad_ide_root_directory