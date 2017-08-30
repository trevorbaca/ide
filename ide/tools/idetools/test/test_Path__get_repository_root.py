import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_Path__get_repository_root_01():

    directory_1 = ide.PackagePath('red_score')._get_repository_root()
    directory_2 = pathlib.Path(ide.__path__[0]).parent
    assert directory_1 == directory_2
