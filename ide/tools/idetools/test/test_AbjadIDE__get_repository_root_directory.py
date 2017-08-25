import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE__get_repository_root_directory_01():

    path = ide.Path('red_score')
    directory_1 = abjad_ide._get_repository_root_directory(path)
    directory_2 = pathlib.Path(ide.__path__[0]).parent
    assert directory_1 == directory_2
