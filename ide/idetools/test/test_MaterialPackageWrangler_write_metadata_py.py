# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_write_metadata_py_01():

    metadata_py_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'red~example~score m mdw y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents