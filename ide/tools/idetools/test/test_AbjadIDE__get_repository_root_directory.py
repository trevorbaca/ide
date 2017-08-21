import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE__get_repository_root_directory_01():

    score_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        )
    directory_1 = abjad_ide._get_repository_root_directory(score_path)
    directory_2 = pathlib.Path(ide.__path__[0]).parent
    assert directory_1 == directory_2
