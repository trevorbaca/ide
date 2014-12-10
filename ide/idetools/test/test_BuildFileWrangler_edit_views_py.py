# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_edit_views_py_01():

    input_ = 'uu we q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_BuildFileWrangler_edit_views_py_02():

    input_ = 'blue~example~score u we q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert not abjad_ide._session._attempted_to_open_file
    assert 'No __views.py__ found.' in contents