# -*- coding: utf-8 -*-
from abjad import *
import ide


def test_AbjadIDE_git_revert_every_asset_01():

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'revert* q'
    abjad_ide._run_main_menu(input_=input_)
    assert abjad_ide._session._attempted_method == 'git_revert_every_package'