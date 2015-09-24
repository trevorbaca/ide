# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_material_directory_01():

    input_ = 'red~example~score %magic q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory - magic numbers',
        ]

    assert abjad_ide._io_manager._transcript.titles == titles
    assert not abjad_ide._session._attempted_to_open_file