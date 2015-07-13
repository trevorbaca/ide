# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_write_enclosing_artifacts_01():

    outer_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        )
    file_names = [
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        ]
    enclosing_artifact_paths = []
    for file_name in file_names:
        path = os.path.join(outer_path, file_name)
        enclosing_artifact_paths.append(path)

    for path in enclosing_artifact_paths:
        assert os.path.isfile(path)

    with systemtools.FilesystemState(keep=enclosing_artifact_paths):
        for path in enclosing_artifact_paths:
            os.remove(path)
        for path in enclosing_artifact_paths:
            assert not os.path.exists(path)
        input_ = 'red~example~score pw q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        for path in enclosing_artifact_paths:
            assert os.path.isfile(path)

    assert 'Wrote enclosing artifacts.' in contents