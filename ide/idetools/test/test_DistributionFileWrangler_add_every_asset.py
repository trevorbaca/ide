# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_DistributionFileWrangler_add_every_asset_01():
    r'''Flow control reaches method in score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score d rad* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_add


def test_DistributionFileWrangler_add_every_asset_02():
    r'''Flow control reaches method in library.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'dd rad* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_add