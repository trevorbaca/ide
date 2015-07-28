# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
configuration = ide.tools.idetools.Configuration()
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_push_score_pdf_to_distribution_directory_01():
    r'''Works in score package.
    '''

    distribution_score_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    assert os.path.exists(distribution_score_path)

    with systemtools.FilesystemState(keep=[distribution_score_path]):
        os.remove(distribution_score_path)
        input_ = 'red~example~score u sp q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(distribution_score_path)
        contents = abjad_ide._transcript.contents
        assert 'Copied' in contents
        assert 'FROM' in contents
        assert 'TO' in contents