# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_edit_every_init_py_01():

    input_ = 'red~example~score g ne* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'Will open ...'
    assert string in contents
    assert abjad_ide._session._attempted_to_open_file