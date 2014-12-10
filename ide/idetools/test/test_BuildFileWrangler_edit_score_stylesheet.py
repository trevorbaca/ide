# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_edit_score_stylesheet_01():

    input_ = 'red~example~score u sse q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file