import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_interpret_lys_01():
    r'''In materials directory.
    '''

    with ide.Test():
        sources = [
            ide.Path('red_score', 'materials', name, 'illustration.ly')
            for name in ['magic_numbers', 'ranges', 'tempi']
            ]
        targets = [_.with_suffix('.pdf') for _ in sources]
        for target in targets:
            target.remove()

        abjad_ide('red mm lyi* q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting every ly ...' in transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' not in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)

        abjad_ide('red mm lyi* q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting every ly ...' in transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)


def test_AbjadIDE_interpret_lys_02():
    r'''In segments directory.
    '''

    with ide.Test():
        sources = [
            ide.Path('red_score', 'segments', name, 'illustration.ly')
            for name in ['A', 'B', 'C']
            ]
        targets = [_.with_suffix('.pdf') for _ in sources]
        for target in targets:
            target.remove()

        abjad_ide('red gg lyi* q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting every ly ...' in transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' not in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)

        abjad_ide('red gg lyi* q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting every ly ...' in transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)
