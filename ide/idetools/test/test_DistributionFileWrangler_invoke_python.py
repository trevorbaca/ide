# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_invoke_python_01():
    
    input_ = 'red~example~score d py 2**38 q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert '274877906944' in contents


def test_DistributionFileWrangler_invoke_python_02():
    
    input_ = 'dd py 2**38 q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert '274877906944' in contents