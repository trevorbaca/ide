# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_invoke_shell_01():

    input_ = 'red~example~score m tempo~inventory !pwd q'
    abjad_ide._run_main_menu(input_=input_)

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents