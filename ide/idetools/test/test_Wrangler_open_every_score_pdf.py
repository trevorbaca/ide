# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_Wrangler_open_every_score_pdf_01():

    input_ = 'so* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Will open ...' in contents
    assert abjad_ide._session._attempted_to_open_file