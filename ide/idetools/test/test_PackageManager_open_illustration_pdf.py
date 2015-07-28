# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageManager_open_illustration_pdf_01():
    r'''In material package.
    '''

    input_ = 'red~example~score m magic~numbers io q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_PackageManager_open_illustration_pdf_02():
    r'''In segment package.
    '''

    input_ = 'red~example~score g A o q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file