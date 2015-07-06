# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)

foo_path = os.path.join(
    abjad_ide._configuration.example_score_packages_directory,
    'red_example_score',
    'red_example_score',
    'build',
    'test_foo.txt',
    )


def test_BuildFileWrangler_remove_every_unadded_asset_01():
    r'''In score.
    '''

    with systemtools.FilesystemState(remove=[foo_path]):
        with open(foo_path, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(foo_path)
        input_ = 'red~example~score u rcn* y q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(foo_path)


def test_BuildFileWrangler_remove_every_unadded_asset_02():
    r'''Out of score.
    '''

    input_ = 'uu rcn* q'
    abjad_ide._run(input_=input_)
    assert abjad_ide._session._attempted_remove_unadded_assets