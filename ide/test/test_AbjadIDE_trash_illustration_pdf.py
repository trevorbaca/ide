import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_illustration_pdf_01():
    """
    In segment directory.
    """

    with ide.Test():
        path = ide.Path('red_score', 'segments', 'A', 'illustration.pdf')
        assert not path.exists()

        path.write_text('')
        assert path.is_file()

        abjad_ide('red %A ipt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()

        abjad_ide('red %A ipt q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {path.trim()} ...' in transcript


def test_AbjadIDE_trash_illustration_pdf_02():
    """
    In segments directory.
    """

    with ide.Test():
        paths = []
        for name in ['_', 'A', 'B']:
            path = ide.Path('red_score', 'segments', name, 'illustration.pdf')
            paths.append(path)

        for path in paths:
            assert not path.exists()
            path.write_text('')
            assert path.is_file()

        abjad_ide('red gg ipt q')
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f'Trashing {path.trim()} ...' in transcript
            assert not path.exists()

        abjad_ide('red gg ipt q')
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f'Missing {path.trim()} ...' in transcript
            assert not path.exists()
