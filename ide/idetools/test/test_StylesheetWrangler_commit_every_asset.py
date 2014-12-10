# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_commit_every_asset_01():
    r'''Works in score.
    '''

    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score y rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit


def test_StylesheetWrangler_commit_every_asset_02():
    r'''Works in library.
    '''

    abjad_ide._session._is_repository_test = True
    input_ = 'yy rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit