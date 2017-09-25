import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_lys_01():

    with ide.Test():
        paths = [
            ide.Path('red_score').segments(name, 'illustration.ly')
            for name in ['A', 'B', 'C']
            ]
        for path in paths:
            assert path.is_file()

        abjad_ide('red gg lyt* q')
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert not path.exists()
            assert f'Trashing {path.trim()} ...' in transcript

        abjad_ide('red gg lyt* q')
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f'Missing {path.trim()} ...' in transcript
