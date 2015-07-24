# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler_go_to_all_materials_01():
    r'''From scores to materials depot.
    '''

    input_ = 'mm q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        ]
    assert abjad_ide._transcript.titles == titles