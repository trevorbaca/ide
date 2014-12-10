# -*- encoding: utf-8 -*-
from abjad import *
import ide
ide = ide.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_every_asset_status_01():

    input_ = 'hh rst* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents