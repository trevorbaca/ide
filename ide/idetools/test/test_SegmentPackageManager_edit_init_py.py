# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_edit_init_py_01():
    r'''Works when __init__.py doesn't exist.
    '''

    input_ = 'red~example~score g A ne q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'Can not find' in contents