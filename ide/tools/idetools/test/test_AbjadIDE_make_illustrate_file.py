import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_illustrate_file_01():

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with ide.Test():
        assert path.is_file()
        path.unlink()
        assert not path.exists()
        input_ = 'red~score mm magic~numbers illm q'
        abjad_ide._start(input_=input_)

    assert path.is_file()
    contents = abjad_ide._io_manager._transcript.contents
    assert '1: __illustrate__.py' in contents


def test_AbjadIDE_make_illustrate_file_02():
    r'''Does not overwrite existing illustrate file.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with ide.Test():
        assert path.is_file()
        input_ = 'red~score mm magic~numbers illm q'
        abjad_ide._start(input_=input_)

    assert path.is_file()
    contents = abjad_ide._io_manager._transcript.contents
    assert 'File already exists:' in contents
