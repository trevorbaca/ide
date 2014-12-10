# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_write_metadata_py_01():

    metadata_py_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        '__metadata__.py',
        )

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'red~example~score k mdw y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents