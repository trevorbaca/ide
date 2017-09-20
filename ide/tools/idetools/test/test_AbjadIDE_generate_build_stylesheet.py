import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_build_stylesheet_01():

    with ide.Test():
        source = ide.Path('boilerplate') / 'build-stylesheet.ily'
        text = source.read_text()
        assert 'paper_size' in text
        assert '"letter"' not in text
        target = ide.Path('blue_score').build('letter', 'stylesheet.ily')
        target.remove()

        abjad_ide('blue~score %letter yg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating stylesheet ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '"letter"' in text

        abjad_ide('blue~score %letter yg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating stylesheet ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '"letter"' in text
