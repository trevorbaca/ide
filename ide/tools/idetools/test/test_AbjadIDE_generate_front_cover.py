import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_front_cover_01():

    with ide.Test():
        target = ide.Path('red_score').build / 'letter' / 'front-cover.tex'
        target.remove()

        input_ = 'red~score %letter fcg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating front cover ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()

        input_ = 'red~score %letter fcg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating front cover ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
