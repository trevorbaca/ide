# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_remove_files_01():

    abjad_ide._session._is_repository_test = True
    input_ = 'yy rm q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_remove