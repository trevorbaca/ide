# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_write_views_py_01():

    input_ = 'red~example~score u ww y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Will write ...' in contents
    assert 'Wrote' in contents