# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler_copy_package_01():

    pretty_path = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'pretty_example_score',
        )

    with systemtools.FilesystemState(remove=[pretty_path]):
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(pretty_path)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=pretty_path, session=abjad_ide._session)
        title = 'Pretty Example Score'
        manager._add_metadatum('title', title)
        input_ = 'rm Pretty~Example~Score remove q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(pretty_path)