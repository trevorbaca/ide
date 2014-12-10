# -*- encoding: utf-8 -*-
from abjad import *
import abjadide


def test_DistributionFileWrangler_add_every_asset_01():
    r'''Flow control reaches method in score.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'red~example~score d rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add


def test_DistributionFileWrangler_add_every_asset_02():
    r'''Flow control reaches method in library.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'dd rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add