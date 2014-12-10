# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_forces_tagline_01():

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        )
    metadata_path = os.path.join(path, '__metadata__.py')

    manager = abjad_ide.idetools.ScorePackageManager
    manager = manager(path=path, session=abjad_ide._session)
    assert manager._get_metadatum('forces_tagline') == 'for piano'

    with systemtools.FilesystemState(keep=[metadata_path]):
        input_ = 'red~example~score p tagline for~foo~bar q'
        abjad_ide._run(input_=input_)
        session = abjad_ide.idetools.Session(is_test=True)
        assert manager._get_metadatum('forces_tagline') == 'for foo bar'