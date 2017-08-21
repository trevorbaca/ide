import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_every_ly_01():
    r'''In materials directory.

    LilyPond files exist but PDFs do not exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = pathlib.Path(
        path,
        'red_example_score',
        'red_example_score',
        'materials',
        )
    package_names = (
        'magic_numbers',
        'ranges',
        'tempi',
        )
    ly_paths = [
        pathlib.Path(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.with_suffix('.pdf') for _ in ly_paths]

    with abjad.FilesystemState(keep=ly_paths):
        for path in pdf_paths:
            if path.is_file():
                path.unlink()
        assert not any(_.exists() for _ in pdf_paths)
        input_ = 'red~example~score mm lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(_.is_file() for _ in pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {!s} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents
        message = 'Writing {!s} ...'
        message = message.format(abjad_ide._trim(pdf_path))
        assert message in contents

    assert 'Preserving' not in contents
    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_02():
    r'''In materials directory.

    LilyPond files and PDFs already exists.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = pathlib.Path(
        path,
        'red_example_score',
        'red_example_score',
        'materials',
        )
    package_names = (
        'magic_numbers',
        'ranges',
        'tempi',
        )
    ly_paths = [
        pathlib.Path(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.with_suffix('.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with abjad.FilesystemState(keep=paths):
        # remove existing PDFs
        for pdf_path in pdf_paths:
            pdf_path.unlink()
        # generate PDFs a first time
        input_ = 'red~example~score mm lyi* q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDFs a second time
        input_ = 'red~example~score mm lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {!s} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents
        message = 'Preserving {!s} ...'
        message = message.format(abjad_ide._trim(pdf_path))
        assert message in contents

    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_03():
    r'''In segments directory.

    LilyPond files exist but PDFs do not exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = pathlib.Path(
        path,
        'red_example_score',
        'red_example_score',
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

    with abjad.FilesystemState(keep=ly_paths):
        for path in pdf_paths:
            if path.is_file():
                path.unlink()
        assert not any(_.exists() for _ in pdf_paths)
        input_ = 'red~example~score gg lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(_.is_file() for _ in pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents
        message = 'Writing {!s} ...'
        message = message.format(abjad_ide._trim(pdf_path))
        assert message in contents

    assert 'Preserving' not in contents
    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_04():
    r'''In segments directory.

    LilyPond files and PDFs already exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = pathlib.Path(
        path,
        'red_example_score',
        'red_example_score',
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

    with abjad.FilesystemState(keep=paths):
        # remove existing PDFs
        for pdf_path in pdf_paths:
            pdf_path.unlink()
        # generate PDFs a first time
        input_ = 'red~example~score gg lyi* q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDFs a second time
        input_ = 'red~example~score gg lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {!s} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents
        message = 'Preserving {!s} ...'
        message = message.format(abjad_ide._trim(pdf_path))
        assert message in contents

    assert 'Total time ' in contents
