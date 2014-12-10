# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_ScorePackageWrangler_add_every_asset_01():
    r'''Flow control reaches add.
    '''

    ide = ide.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add