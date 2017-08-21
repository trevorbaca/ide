import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_preface_01():
    r'''Works when preface.pdf doesn't yet exist.
    '''

    tex_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.tex',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.pdf',
        )

    with abjad.FilesystemState(keep=[tex_path, pdf_path]):
        pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~example~score bb letter-portrait pi q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_preface_02():
    r'''Works when preface.pdf already exists.
    '''

    tex_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.tex',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.pdf',
        )

    with abjad.FilesystemState(keep=[tex_path, pdf_path]):
        assert pdf_path.exists()
        input_ = 'red~example~score bb letter-portrait pi q'
        abjad_ide._start(input_=input_)
        assert pdf_path.exists()
