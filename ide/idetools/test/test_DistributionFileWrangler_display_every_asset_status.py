# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_display_every_asset_status_01():
    r'''Works with distribution file library.
    '''

    input_ = 'dd rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_DistributionFileWrangler_display_every_asset_status_02():
    r'''Works with Git-managed score.
    '''

    input_ = 'red~example~score d rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents