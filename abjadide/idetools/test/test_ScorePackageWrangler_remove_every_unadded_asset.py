# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_remove_every_unadded_asset_01():

    input_ = 'rcn* q'
    ide._run(input_=input_)
    assert ide._session._attempted_remove_unadded_assets