import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'tempi' / 'illustration.ly'
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red~score %tempi lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red~score %tempi lyi q')
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
        source = ide.Path('red_score').segments
        source = source / 'segment_01' / 'illustration.ly'
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red~score %A lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red~score %A lyi q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
