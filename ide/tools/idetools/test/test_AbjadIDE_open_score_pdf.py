# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_open_score_pdf_01():

    input_ = 'red~example~score so q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_score_pdf_02():

    input_ = 'blue~example~score so q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string =  "File ending in 'score.pdf' not found." in contents
    assert not abjad_ide._session._attempted_to_open_file