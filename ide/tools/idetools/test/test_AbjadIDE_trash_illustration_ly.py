import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_illustration_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        path = ide.Path('red_score')
        path = path('materials', 'red_pitch_classes', 'illustration.ly')
        assert path.is_file()

        abjad_ide('red %rpc lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()

        abjad_ide('red %rpc lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {path.trim()} ...' in transcript


def test_AbjadIDE_trash_illustration_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        path = ide.Path('red_score', 'segments', 'A', 'illustration.ly')
        assert path.is_file()

        abjad_ide('red %A lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()

        abjad_ide('red %A lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {path.trim()} ...' in transcript
