# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_open_every_score_pdf_01():

    red_score_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    input_ = 'pdf* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert abjad_ide._session._attempted_to_open_file
    message = 'Opening {} ...'
    message = message.format(abjad_ide._trim_path(red_score_path))
    assert message in contents