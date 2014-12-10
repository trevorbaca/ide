# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_MaterialPackageWrangler_add_every_asset_01():
    r'''Works in score.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'red~example~score m rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add


def test_MaterialPackageWrangler_add_every_asset_02():
    r'''Works in library.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'mm rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add