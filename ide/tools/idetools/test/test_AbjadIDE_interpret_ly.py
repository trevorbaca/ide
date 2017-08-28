import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'tempi' / 'illustration.ly'
        target = source.with_suffix('.pdf')
        target.remove()

        input_ = 'red~score %tempi lyi q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {abjad_ide._trim(source)} ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()

        input_ = 'red~score %tempi lyi q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {abjad_ide._trim(source)} ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()


def test_AbjadIDE_interpret_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments
        source = source / 'segment_01' / 'illustration.ly'
        target = source.with_suffix('.pdf')
        target.remove()

        input_ = 'red~score %A lyi q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {abjad_ide._trim(source)} ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()

        input_ = 'red~score %A lyi q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Interpreting ly ...' in transcript
        assert f'Interpreting {abjad_ide._trim(source)} ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
