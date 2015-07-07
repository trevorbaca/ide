# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_MaterialPackageWrangler_display_every_asset_status_01():
    r'''Work with Git outside of score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'mm rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_02():
    r'''Work with Git inside score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents