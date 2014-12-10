# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
abjad_ide._session._is_repository_test = True


def test_MaterialPackageWrangler_update_every_asset_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score m rup* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_update


def test_MaterialPackageWrangler_update_every_asset_02():
    r'''Works in library.
    '''

    input_ = 'mm rup* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_update