# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_SegmentPackageWrangler_commit_every_asset_01():
    r'''Works in score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score g rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit


def test_SegmentPackageWrangler_commit_every_asset_02():
    r'''Works in library.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'gg rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit