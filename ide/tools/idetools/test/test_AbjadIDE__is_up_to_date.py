# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE__is_up_to_date_01():

    path = abjad_ide._find_up_to_date_path('scores', system=True)
    temporary_file = os.path.join(path, 'test_temporary.txt')

    assert abjad_ide._is_up_to_date(path)
    assert not os.path.exists(temporary_file)

    with systemtools.FilesystemState(remove=[temporary_file]):
        with open(temporary_file, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(temporary_file)
        assert not abjad_ide._is_up_to_date(path)