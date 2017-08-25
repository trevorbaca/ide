import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_every_pdf_01():
    r'''In materials directory.

    Neither LilyPond files nor PDFs exist.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        )
    # only this package has an illustrate file
    package_names = (
        'magic_numbers',
        )
    ly_paths = [
        pathlib.Path(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.with_suffix('.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with ide.Test():
        input_ = 'red~score mm pdfm* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(_.is_file() for _ in paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Removing {} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents

    assert 'Opening' not in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_every_pdf_02():
    r'''In segments directory.

    Neither LilyPond files nor PDFs exist.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        )
    package_names = (
        'segment_01',
        'segment_02',
        'segment_03',
        )
    ly_paths = [
        pathlib.Path(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.with_suffix('.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with ide.Test():
        for path in paths:
            if path.exists():
                path.unlink()
        assert not any(_.exists() for _ in paths)
        input_ = 'red~score gg pdfm* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(_.is_file() for _ in paths)

    assert 'Opening' not in contents
    assert 'Total time ' in contents
