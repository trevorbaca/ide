import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_trash_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        path = ide.Path('red_score')
        path = path / 'materials' / 'magic_numbers' / 'illustration.ly'
        assert path.is_file()
        input_ = 'red~score %magic~numbers lyt q'
        abjad_ide._start(input_=input_)
        assert not path.exists()


def test_AbjadIDE_trash_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        path = ide.Path('red_score')
        path = path / 'segments' / 'segment_01' / 'illustration.ly'
        assert path.is_file()
        input_ = 'red~score %A lyt q'
        abjad_ide._start(input_=input_)
        assert not path.exists()
