import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_generate_back_cover_01():

    with ide.Test():
        source = ide.Path('boilerplate') / 'back-cover.tex'
        text = source.read_text()
        assert 'paper_size' in text
        assert '{8.5in, 11in}' not in text
        target = ide.Path('blue_score').builds('letter', 'back-cover.tex')
        target.remove()

        abjad_ide('blue~score %letter bcg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating back cover ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '{8.5in, 11in}' in text

        abjad_ide('blue~score %letter bcg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating back cover ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '{8.5in, 11in}' in text
