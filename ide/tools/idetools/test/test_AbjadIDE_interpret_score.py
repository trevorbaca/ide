import abjad
import ide
import pathlib
import shutil
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_score_01():
    r'''Works when score.pdf doesn't yet exist.
    '''

    tex_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.tex',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.pdf',
        )

    with abjad.FilesystemState(keep=[tex_path, pdf_path]):
        pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_score_02():
    r'''Works when score.pdf already exists.
    '''

    tex_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.tex',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.pdf',
        )

    with abjad.FilesystemState(keep=[tex_path, pdf_path]):
        assert pdf_path.exists()
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        assert pdf_path.exists()


def test_AbjadIDE_interpret_score_03():
    r'''LaTeX error does not freeze IDE.
    '''

    bad_score_tex_path = pathlib.Path(
        configuration.abjad_ide_directory,
        'boilerplate',
        'bad-score.tex',
        )
    score_tex_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.tex',
        )
    score_pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.pdf',
        )
    paths = [score_tex_path, score_pdf_path]

    with abjad.FilesystemState(keep=paths):
        shutil.copyfile(str(bad_score_tex_path), str(score_tex_path))
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'ERROR IN LATEX LOG FILE ...' in contents
