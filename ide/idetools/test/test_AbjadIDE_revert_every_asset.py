# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_revert_every_asset_01():

    abjad_ide._session._is_repository_test = True
    input_ = 'hh rrv* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_revert