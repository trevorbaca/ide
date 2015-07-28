# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageManager_edit_score_stylesheet_01():
    r'''In material package.
    '''

    input_ = 'red~example~score m tempo~inventory sse q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_PackageManager_edit_score_stylesheet_02():
    r'''In segment package.
    '''

    input_ = 'red~example~score g A sse q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_PackageManager_edit_score_stylesheet_03():
    r'''In score package.
    '''

    input_ = 'red~example~score sse q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file