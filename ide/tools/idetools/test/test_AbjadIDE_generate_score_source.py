# -*- coding: utf-8 -*-
import filecmp
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_score_source_01():
    r'''Works when score source already exists.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'score.tex',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score bb sg q'
        abjad_ide._start_abjad_ide(input_=input_)
        assert os.path.isfile(path)
        assert filecmp.cmp(path, path + '.backup')