# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_quit_01():
    
    input_ = 'red~example~score q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents