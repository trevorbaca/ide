# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_quit_01():
    
    input_ = 'red~example~score m q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents


def test_MaterialPackageWrangler_quit_02():
    
    input_ = 'mm q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents