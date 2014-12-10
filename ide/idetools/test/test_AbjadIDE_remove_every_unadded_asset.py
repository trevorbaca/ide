# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_remove_every_unadded_asset_01():

        input_ = 'hh rcn* q'
        abjad_ide._run(input_=input_)
        assert abjad_ide._session._attempted_remove_unadded_assets