# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_illustrate_py_01():

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score m magic~numbers gl y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(path)
        assert not filecmp.cmp(path, path + '.backup')
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Will generate' in contents
        assert 'Generated' in contents