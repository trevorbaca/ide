# -*- coding: utf-8 -*-
import filecmp
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_illustrate_file_01():

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        assert os.path.isfile(path)
        os.remove(path)
        assert not os.path.isfile(path)
        input_ = 'red~example~score m magic~numbers illm y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(path)