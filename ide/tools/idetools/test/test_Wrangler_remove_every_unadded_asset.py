# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_remove_every_unadded_asset_01():

    input_ = 'clean* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_remove_unadded_assets