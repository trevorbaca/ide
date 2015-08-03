# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Wrangler_git_update_every_package_01():

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'up* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_update