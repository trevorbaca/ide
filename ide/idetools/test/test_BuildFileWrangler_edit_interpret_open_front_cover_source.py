# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_edit_interpret_open_front_cover_source_01():

    tex_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    pdf_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score u fceio q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    assert abjad_ide._session._attempted_to_open_file