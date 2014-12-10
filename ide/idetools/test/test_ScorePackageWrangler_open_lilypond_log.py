# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_open_lilypond_log_01():

    input_ = 'uu ll q'
    abjad_ide._run(input_=input_)
    
    assert abjad_ide._session._attempted_to_open_file