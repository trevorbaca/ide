# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_year_01():

    metadata_file = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        '__metadata__.py',
        )
        
    with systemtools.FilesystemState(keep=[metadata_file]):
        input_ = 'red~example~score p year 2001 q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        string = 'Red Example Score (2001)'
        assert string in contents