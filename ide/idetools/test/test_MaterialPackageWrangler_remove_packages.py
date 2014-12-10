# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_remove_packages_01():

    abjad_ide._session._is_repository_test = True
    input_ = 'red~example~score m rm q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_to_remove