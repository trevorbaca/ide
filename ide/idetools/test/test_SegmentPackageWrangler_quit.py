# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_quit_01():
    
    input_ = 'red~example~score g q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents


def test_SegmentPackageWrangler_quit_02():
    
    input_ = 'gg q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents