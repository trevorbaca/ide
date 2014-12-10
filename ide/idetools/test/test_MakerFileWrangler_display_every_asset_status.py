# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_display_every_asset_status_01():
    r'''Works with library.
    '''

    input_ = 'kk rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MakerFileWrangler_display_every_asset_status_02():
    r'''Works with Git-managed makers directory.
    '''

    input_ = 'red~example~score k rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MakerFileWrangler_display_every_asset_status_03():
    r'''Works with Subversion-managed makers directory.
    '''

    # is_test=False to allow user scores to appear
    abjad_ide = ide.idetools.AbjadIDE(is_test=False)
    score_name = abjad_ide._score_package_wrangler._find_svn_score_name()
    if not score_name:
        return

    input_ = '{} k rst* q'.format(score_name)
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents