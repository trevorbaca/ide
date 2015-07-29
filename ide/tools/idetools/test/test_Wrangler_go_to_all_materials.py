# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_all_materials_01():
    r'''From scores to all material directories.
    '''

    input_ = 'mm q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all material directories',
        ]
    assert abjad_ide._transcript.titles == titles