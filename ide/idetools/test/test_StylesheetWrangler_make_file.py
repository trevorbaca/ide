# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_make_file_01():

    path = os.path.join(
        abjad_ide._configuration.stylesheets_library,
        'test-stylesheet.ily',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'yy new My~stylesheet~library test-stylesheet q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(path)

    assert 'Select storehouse:' in contents


def test_StylesheetWrangler_make_file_02():
    r'''Makes sure that file name 'new-*.ily' doesn't alias command (new).
    '''

    path_1 = os.path.join(
        abjad_ide._configuration.stylesheets_library,
        'new-test-stylesheet-1.ily',
        )
    path_2 = os.path.join(
        abjad_ide._configuration.stylesheets_library,
        'new-test-stylesheet-2.ily',
        )

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        input_ = 'yy new My~stylesheet~library new-test-stylesheet-1 q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(path_1)
        input_ = 'yy new My~stylesheet~library new-test-stylesheet-2 q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(path_2)
        input_ = 'yy new-test-stylesheet-1.ily q'
        abjad_ide._run(input_=input_)
        assert abjad_ide._session._attempted_to_open_file