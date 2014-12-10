# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_ScorePackageWrangler_edit_cache_01():

    ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'ce q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file