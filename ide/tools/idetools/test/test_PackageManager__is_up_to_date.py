# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager__is_up_to_date_01():

    manager = abjad_ide._score_package_wrangler._find_up_to_date_manager(
        system=True,
        )
    temporary_file = os.path.join(manager._path, 'test_temporary.txt')

    assert manager._is_up_to_date(manager._io_manager, manager._path)
    assert not os.path.exists(temporary_file)

    with systemtools.FilesystemState(remove=[temporary_file]):
        with open(temporary_file, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(temporary_file)
        assert not manager._is_up_to_date(manager._io_manager, manager._path)