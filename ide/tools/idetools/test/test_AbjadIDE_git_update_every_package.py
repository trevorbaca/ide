# -*- coding: utf-8 -*-
import abjad
import ide


def test_AbjadIDE_git_update_every_package_01():

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'up* q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_method == 'git_update_every_package'