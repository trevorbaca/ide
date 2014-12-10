# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_display_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score rst q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_ScorePackageManager_display_status_02():
    r'''Works with Subversion.
    '''

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=False)
    name = abjad_ide._score_package_wrangler._find_svn_score_name()
    if not name:
        return

    input_ = '{} rst q'.format(name)
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents