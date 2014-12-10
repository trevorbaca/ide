# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_copy_file_01():

    source_path = os.path.join(
        abjad_ide._configuration.example_stylesheets_directory,
        'clean-letter-14.ily',
        )
    target_path = os.path.join(
        abjad_ide._configuration.stylesheets_library,
        'test-foo-stylesheet.ily',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'yy cp clean-letter-14.ily'
        input_ += ' My~stylesheet~library test~foo~stylesheet y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'test-foo-stylesheet.ily' in contents