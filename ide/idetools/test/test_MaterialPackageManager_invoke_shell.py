# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_invoke_shell_01():

    input_ = 'red~example~score m tempo~inventory !pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents