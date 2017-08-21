import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_trash_ly_01():
    r'''In material directory.
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
        assert ly_path.is_file()
        input_ = 'red~example~score mm magic~numbers lyt q'
        abjad_ide._start(input_=input_)
        assert not ly_path.exists()


def test_AbjadIDE_trash_ly_02():
    r'''In segment directory.
    '''

    material_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = pathlib.Path(material_directory, 'illustration.ly')

    with abjad.FilesystemState(keep=[ly_path]):
        assert ly_path.is_file()
        input_ = 'red~example~score gg A lyt q'
        abjad_ide._start(input_=input_)
        assert not ly_path.exists()
