import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_interpret_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path(
            'red_score', 'materials', 'metronome_marks', 'illustration.ly')
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red %metronome lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red %metronome lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()


def test_AbjadIDE_interpret_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'segments', 'A', 'illustration.ly')
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red %A lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red %A lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
