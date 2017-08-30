import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_front_cover_01():

    with ide.Test():
        target = ide.PackagePath('red_score').builds / 'letter' / 'front-cover.tex'
        target.remove()

        input_ = 'red~score %letter fcg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating front cover ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()

        input_ = 'red~score %letter fcg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating front cover ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
