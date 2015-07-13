# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_make_file_01():
    r'''Makes file with Unicode header.
    '''

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'makers',
        'FooMaker.py',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score k new FooMaker.py q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(path)
        contents = ''.join(file(path, 'r').readlines())
        directive = abjad_ide._configuration.unicode_directive
        assert directive in contents