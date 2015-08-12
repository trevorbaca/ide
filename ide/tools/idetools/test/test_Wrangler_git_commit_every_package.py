# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Wrangler_git_commit_every_package_01():

    abjad_ide = ide.tools.idetools.Controller(is_test=True)
    abjad_ide._session._is_repository_test = True
    input_ = 'ci* q'
    abjad_ide._run_main_menu(input_=input_)
    assert abjad_ide._session._attempted_to_commit