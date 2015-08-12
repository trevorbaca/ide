# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.Controller(is_test=True)


def test_Wrangler_git_status_every_package_01():
    r'''Works with all scores.
    '''

    input_ = 'st* q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents