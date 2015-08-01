# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_home_01():

    input_ = 'h q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._session._transcript.titles == titles