# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_open_every_score_pdf_01():

    input_ = 'so* y q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Will open ...' in contents
    assert abjad_ide._session._attempted_to_open_file