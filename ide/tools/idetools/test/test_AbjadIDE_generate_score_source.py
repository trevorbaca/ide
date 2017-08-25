import filecmp
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_score_source_01():
    r'''Works when score source already exists.
    '''

    path = ide.Path('red_score').build / 'letter' / 'score.tex'
    with ide.Test(keep=[path]):
        if path.exists():
            path.unlink()
        input_ = 'red~score bb letter sg q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        assert filecmp.cmp(str(path), str(path) + '.backup')
