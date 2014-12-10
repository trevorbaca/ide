# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_open_draft_pdf_01():

    input_ = 'red~example~score u do q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file