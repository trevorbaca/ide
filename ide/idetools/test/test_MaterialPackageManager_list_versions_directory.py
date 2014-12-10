# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_MaterialPackageManager_list_versions_directory_01():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers vl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'definition_0001.py output_0001.py'
    assert string in contents

    
def test_MaterialPackageManager_list_versions_directory_02():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory vl q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'illustration_0001.ly illustration_0001.pdf output_0001.py'
    assert string in contents