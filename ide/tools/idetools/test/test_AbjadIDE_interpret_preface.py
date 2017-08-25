import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_preface_01():
    r'''Works when preface.pdf doesn't yet exist.
    '''

    tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'preface.tex',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'preface.pdf',
        )

    with ide.Test():
        if pdf_path.exists():
            pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~score bb letter pi q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()


def test_AbjadIDE_interpret_preface_02():
    r'''Works when preface.pdf already exists.
    '''

    tex_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'preface.tex',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'preface.pdf',
        )

    with ide.Test():
        assert pdf_path.exists()
        input_ = 'red~score bb letter pi q'
        abjad_ide._start(input_=input_)
        assert pdf_path.exists()
