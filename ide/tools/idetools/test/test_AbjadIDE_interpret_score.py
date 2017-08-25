import ide
import pathlib
import shutil
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_score_01():
    r'''Works when score.pdf doesn't yet exist.
    '''

    tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'score.tex',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'score.pdf',
        )

    with ide.Test():
        if pdf_path.exists():
            pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~score bb letter si q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()


def test_AbjadIDE_interpret_score_02():
    r'''Works when score.pdf already exists.
    '''

    tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'score.tex',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'score.pdf',
        )

    with ide.Test():
        assert pdf_path.exists()
        input_ = 'red~score bb letter si q'
        abjad_ide._start(input_=input_)
        assert pdf_path.exists()


def test_AbjadIDE_interpret_score_03():
    r'''LaTeX error does not freeze IDE.
    '''

    bad_score_tex_path = pathlib.Path(
        abjad_ide.configuration.boilerplate_directory,
        'bad-score.tex',
        )
    score_tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'score.tex',
        )
    score_pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'score.pdf',
        )
    paths = [score_tex_path, score_pdf_path]

    with ide.Test():
        shutil.copyfile(str(bad_score_tex_path), str(score_tex_path))
        input_ = 'red~score bb letter si q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'ERROR IN LATEX LOG FILE ...' in contents
