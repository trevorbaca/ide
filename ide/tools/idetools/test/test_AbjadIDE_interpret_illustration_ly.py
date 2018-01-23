import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_interpret_illustration_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path(
            'red_score', 'materials', 'metronome_marks', 'illustration.ly')
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red %metronome ili q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red %metronome ili q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()


def test_AbjadIDE_interpret_illustration_ly_02():
    r'''In materials directory.
    '''

    with ide.Test():
        sources = [
            ide.Path('red_score', 'materials', name, 'illustration.ly')
            for name in ['red_pitch_classes', 'metronome_marks']
            ]
        targets = [_.with_suffix('.pdf') for _ in sources]
        for target in targets:
            target.remove()

        abjad_ide('red mm ili q')
        transcript = abjad_ide.io.transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' not in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)

        abjad_ide('red mm ili q')
        transcript = abjad_ide.io.transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)


def test_AbjadIDE_interpret_illustration_ly_03():
    r'''In segments directory.
    '''

    with ide.Test():
        sources = []
        for name in ['_', 'A', 'B']:
            path = ide.Path('red_score', 'segments', name, 'illustration.ly')
            sources.append(path)
        targets = [_.with_suffix('.pdf') for _ in sources]
        for target in targets:
            target.remove()

        abjad_ide('red gg ili q')
        transcript = abjad_ide.io.transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' not in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)

        abjad_ide('red gg ili q')
        transcript = abjad_ide.io.transcript
        for source, target in zip(sources, targets):
            assert 'Interpreting ly ...' in transcript
            assert f'Removing {target.trim()} ...' in transcript
            assert f'Interpreting {source.trim()} ...' in transcript
            assert f'Writing {target.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
        assert 'Total time' in transcript
        assert all(_.is_file() for _ in targets)


def test_AbjadIDE_interpret_illustration_ly_04():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'segments', 'A', 'illustration.ly')
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red %A ili q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red %A ili q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
