# -*- coding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_push_score_pdf_to_distribution_directory_01():
    r'''Works in score package.
    '''

    distribution_score_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    assert os.path.exists(distribution_score_path)

    with systemtools.FilesystemState(keep=[distribution_score_path]):
        os.remove(distribution_score_path)
        input_ = 'red~example~score bb sp q'
        abjad_ide._start_abjad_ide(input_=input_)
        assert os.path.exists(distribution_score_path)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Copied' in contents
        assert 'FROM' in contents
        assert 'TO' in contents