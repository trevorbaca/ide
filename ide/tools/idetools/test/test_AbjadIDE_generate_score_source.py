# -*- coding: utf-8 -*-
import abjad
import filecmp
import ide
import os
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
        'letter-portrait',
        'score.tex',
        )

    with abjad.systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score bb letter-portrait sg q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(path)
        assert filecmp.cmp(path, path + '.backup')
