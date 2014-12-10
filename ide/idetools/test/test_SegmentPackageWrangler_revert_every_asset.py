# -*- encoding: utf-8 -*-
import ide


def test_SegmentPackageWrangler_revert_every_asset_01():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score g rrv* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_revert


def test_SegmentPackageWrangler_revert_every_asset_02():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'gg rrv* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_revert