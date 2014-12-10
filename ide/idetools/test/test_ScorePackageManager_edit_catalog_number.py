# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_catalog_number_01():

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        )
    metadata_path = os.path.join(path, '__metadata__.py')

    manager = ide.idetools.ScorePackageManager
    manager = manager(path=path, session=abjad_ide._session)
    assert manager._get_metadatum('catalog_number') == '\#165'

    with systemtools.FilesystemState(keep=[metadata_path]):
        input_ = 'red~example~score p catalog~number for~foo~bar q'
        abjad_ide._run(input_=input_)
        session = ide.idetools.Session(is_test=True)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._get_metadatum('catalog_number') == 'for foo bar'