import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        target = ide.Path('red_score').materials('magic_numbers')
        target /= 'illustration.ly'
        assert target.is_file()

        abjad_ide('red %magic lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {target.trim()} ...' in transcript
        assert not target.exists()

        abjad_ide('red %magic lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {target.trim()} ...' in transcript


def test_AbjadIDE_trash_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        target = ide.Path('red_score').segments('A', 'illustration.ly')
        assert target.is_file()

        abjad_ide('red %A lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {target.trim()} ...' in transcript
        assert not target.exists()

        abjad_ide('red %A lyt q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {target.trim()} ...' in transcript
