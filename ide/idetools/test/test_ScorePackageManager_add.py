# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_add_01():
    r'''Add two files to Git-managed score package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the score package as found.
    '''

    manager = abjad_ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert manager._test_add()


def test_ScorePackageManager_add_02():
    r'''Displays informative message when nothing to add.
    '''

    input_ = 'red~example~score rad q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Nothing to add.' in contents