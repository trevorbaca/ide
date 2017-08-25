import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_every_ly_01():
    r'''In materials directory.
    '''

    path = abjad_ide.configuration.example_scores_directory
    path = pathlib.Path(
        path,
        'red_score',
        'red_score',
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

    with ide.Test():
        for path in pdf_paths:
            if path.is_file():
                path.unlink()
        assert not any(_.exists() for _ in pdf_paths)
        input_ = 'red~score mm lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(_.is_file() for _ in pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim(pdf_path))
        assert message in contents

    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_02():
    r'''In segments directory.
    '''

    path = abjad_ide.configuration.example_scores_directory
    path = pathlib.Path(
        path,
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

    with ide.Test():
        for path in pdf_paths:
            if path.is_file():
                path.unlink()
        assert not any(_.exists() for _ in pdf_paths)
        input_ = 'red~score gg lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(_.is_file() for _ in pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim(ly_path))
        assert message in contents
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim(pdf_path))
        assert message in contents

    assert 'Total time ' in contents
