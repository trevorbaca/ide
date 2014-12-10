# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide


def test_ScorePackageWrangler_add_every_asset_01():
    r'''Flow control reaches add.
    '''

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'rad* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_add