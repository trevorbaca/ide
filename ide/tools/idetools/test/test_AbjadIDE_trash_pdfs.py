import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_pdfs_01():

    with ide.Test():
        paths = [
            ide.Path('red_score', 'segments', name, 'illustration.pdf')
            for name in ['A', 'B', 'C']
            ]
        for path in paths:
            path.remove()

        abjad_ide('red gg pdft* q')
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f'Missing {path.trim()} ...' in transcript
