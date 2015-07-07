# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_display_every_asset_status_01():
    r'''Works in segments depot.
    '''

    input_ = 'gg rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_SegmentPackageWrangler_display_every_asset_status_02():
    r'''Works with Git-managed segment package.
    '''

    input_ = 'red~example~score g rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents