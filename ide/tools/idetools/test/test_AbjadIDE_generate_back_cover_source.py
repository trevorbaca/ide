import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_back_cover_source_01():

    with ide.Test():
        source = ide.Path('boilerplate') / 'back-cover.tex'
        text = source.read_text()
        assert 'paper_size' in text
        assert '{8.5in, 11in}' not in text
        target = ide.Path('blue_score').build / 'letter' / 'back-cover.tex'
        if target.exists():
            target.unlink()
        input_ = 'blue~score %letter bcg q'
        abjad_ide._start(input_=input_)
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '{8.5in, 11in}' in text
        contents = abjad_ide._io_manager._transcript.contents
        assert f'Removing {abjad_ide._trim(target)} ...' not in contents
        assert f'Writing {abjad_ide._trim(target)} ...' in contents
        input_ = 'blue~score %letter bcg q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert f'Removing {abjad_ide._trim(target)} ...' in contents
        assert f'Writing {abjad_ide._trim(target)} ...' in contents
