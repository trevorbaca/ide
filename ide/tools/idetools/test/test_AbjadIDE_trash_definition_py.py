import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_definition_py_01():

    with ide.Test():
        path = ide.Path('red_score', 'segments', 'A', 'definition.py')
        assert path.is_file()

        abjad_ide('red %A dft q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()

        abjad_ide('red %A dft q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {path.trim()} ...' in transcript
