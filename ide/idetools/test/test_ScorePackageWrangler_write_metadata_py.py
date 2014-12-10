# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_write_metadata_py_01():

    input_ = 'mdw y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Will write ...' in contents
    assert abjad_ide._configuration.wrangler_views_metadata_file in contents