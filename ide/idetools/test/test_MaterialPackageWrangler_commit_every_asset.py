# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_MaterialPackageWrangler_commit_every_asset_01():
    r'''Works in score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score m rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit


def test_MaterialPackageWrangler_commit_every_asset_02():
    r'''Works in library.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'mm rci* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_commit