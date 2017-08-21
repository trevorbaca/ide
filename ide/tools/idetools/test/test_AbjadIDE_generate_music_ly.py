import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_music_ly_01():
    r'''When music does not exist yet.

    (Can't use filecmp because music.ly file contains LilyPond version
    directive, LilyPond language directive and file paths. All depend
    on user environment.)
    '''

    music_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'music.ly',
        )

    with abjad.FilesystemState(keep=[music_path]):
        music_path.unlink()
        input_ = 'red~example~score bb letter-portrait mg q'
        abjad_ide._start(input_=input_)
        assert music_path.is_file()
        with music_path.open() as file_pointer:
            file_lines = file_pointer.readlines()
            file_contents = ''.join(file_lines)
        assert 'Red Example Score (2013) for piano' in file_contents
        assert r'\language' in file_contents
        assert r'\version' in file_contents


def test_AbjadIDE_generate_music_ly_03():
    r'''Indents include files exacty four spaces.
    '''

    music_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'music.ly',
        )

    with abjad.FilesystemState(keep=[music_path]):
        input_ = 'red~example~score bb letter-portrait mg q'
        abjad_ide._start(input_=input_)

    with music_path.open() as file_pointer:
        file_lines = file_pointer.readlines()
        file_contents = ''.join(file_lines)
        tab = 4 * ' '
        line = '\n' + tab + r'\include'
        assert line in file_contents
