import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_ly_01():
    r'''In material directory.

    Creates LilyPond file when none exists.
    '''

    material_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(material_directory, 'illustration.ly')

    with abjad.FilesystemState(keep=[ly_path]):
        ly_path.unlink()
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Overwriting' in contents
    assert str(abjad_ide._trim(ly_path)) in contents


def test_AbjadIDE_make_ly_02():
    r'''In material directory.

    Preserves existing LilyPond file when candidate compares the same.
    '''

    material_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(material_directory, 'illustration.ly')
    candidate_ly_path = pathlib.Path(
        material_directory,
        'illustration.candidate.ly',
        )

    with abjad.FilesystemState(keep=[ly_path]):
        # remove existing ly
        ly_path.unlink()
        assert not ly_path.exists()
        # generate ly first time
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        # attempt to generate ly second time (but blocked)
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert str(abjad_ide._trim(ly_path)) in contents
    assert str(abjad_ide._trim(candidate_ly_path)) in contents
    assert '... compare the same.' in contents


def test_AbjadIDE_make_ly_03():
    r'''In material directory.

    Prompts composer to overwrite existing PDF when candidate compares
    differently.
    '''

    material_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(material_directory, 'illustration.ly')
    candidate_ly_path = pathlib.Path(
        material_directory,
        'illustration.candidate.ly',
        )

    with abjad.FilesystemState(keep=[ly_path]):
        with ly_path.open('w') as file_pointer:
            file_pointer.write('text')
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert str(abjad_ide._trim(ly_path)) in contents
    assert str(abjad_ide._trim(candidate_ly_path)) in contents
    assert '... compare differently.' in contents


def test_AbjadIDE_make_ly_04():
    r'''In segment directory.

    Creates LilyPond file when none exists.
    '''

    segment_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')

    with abjad.FilesystemState(keep=[ly_path]):
        ly_path.unlink()
        input_ = 'red~example~score gg A lym q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Wrote' in contents
    assert str(abjad_ide._trim(ly_path)) in contents
