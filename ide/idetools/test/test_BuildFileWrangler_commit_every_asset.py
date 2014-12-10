# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_BuildFileWrangler_commit_every_asset_01():
    r'''Works in score.
    '''

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score u rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit


def test_BuildFileWrangler_commit_every_asset_02():
    r'''Works in library.
    '''

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'uu rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit