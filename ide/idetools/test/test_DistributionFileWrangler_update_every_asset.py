# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_DistributionFileWrangler_update_every_asset_01():
    r'''Works in score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score d rup* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_update


def test_DistributionFileWrangler_update_every_asset_02():
    r'''Works in library.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'dd rup* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_update