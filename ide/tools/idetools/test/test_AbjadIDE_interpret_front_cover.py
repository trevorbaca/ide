import ide
import os
import pathlib
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Fails under containerized Travis-CI."
    )
def test_AbjadIDE_interpret_front_cover_01():
    r'''Works when front-cover.pdf doesn't exist yet.
    '''

    tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'front-cover.tex',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'front-cover.pdf',
        )

    with ide.Test():
        pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~score bb letter fci q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Fails under containerized Travis-CI."
    )
def test_AbjadIDE_interpret_front_cover_02():
    r'''Works when front-cover.pdf already exists.
    '''

    tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'front-cover.tex',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'front-cover.pdf',
        )

    with ide.Test():
        assert pdf_path.exists()
        input_ = 'red~score bb letter fci q'
        abjad_ide._start(input_=input_)
        assert pdf_path.exists()
