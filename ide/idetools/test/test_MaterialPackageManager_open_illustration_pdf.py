# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_open_illustration_pdf_01():

    input_ = 'red~example~score m magic~numbers io q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file