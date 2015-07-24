# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_PackageWrangler_add_every_asset_01():
    r'''Flow control reaches add.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'add* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_add