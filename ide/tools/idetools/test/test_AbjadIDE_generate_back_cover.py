import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_back_cover_01():

    with ide.Test():
        source = ide.Path('boilerplate') / 'back-cover.tex'
        text = source.read_text()
        assert 'paper_size' in text
        assert '{8.5in, 11in}' not in text
        target = ide.Path('blue_score').build / 'letter' / 'back-cover.tex'
        target.remove()

        input_ = 'blue~score %letter bcg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating back cover ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '{8.5in, 11in}' in text

        input_ = 'blue~score %letter bcg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating back cover ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '{8.5in, 11in}' in text
