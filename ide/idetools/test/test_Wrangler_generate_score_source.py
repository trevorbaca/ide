# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_Wrangler_generate_score_source_01():
    r'''Works when score source already exists.
    '''

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'score.tex',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score u sg y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(path)
        assert filecmp.cmp(path, path + '.backup')