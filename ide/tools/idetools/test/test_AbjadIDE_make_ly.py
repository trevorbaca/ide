import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_ly_01():
    r'''In material directory.
    '''

    material_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(material_directory, 'illustration.ly')

    with ide.Test(keep=[ly_path]):
        input_ = 'red~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Removing' in contents
    assert 'Writing' in contents
    assert abjad_ide._trim(ly_path) in contents


def test_AbjadIDE_make_ly_02():
    r'''In segment directory.
    '''

    segment_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_01',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')

    with ide.Test(keep=[ly_path]):
        input_ = 'red~score gg A lym q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Wrote' in contents
    assert abjad_ide._trim(ly_path) in contents
