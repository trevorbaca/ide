import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_generate_music_ly_01():

    with ide.Test():
        target = ide.Path('red_score', 'builds', 'letter-score', 'music.ly')
        target.remove()

        abjad_ide('red %letter ggc mlg q')
        transcript = abjad_ide.io.transcript
        assert f'Generating {target.trim()} ...' in transcript
        #assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n        \include "_segments/segment--.ly"' in text
        assert '\n        \include "_segments/segment-A.ly"' in text
        assert '\n        \include "_segments/segment-B.ly"' in text

        abjad_ide('red %letter mlg q')
        transcript = abjad_ide.io.transcript
        assert f'Generating {target.trim()} ...' in transcript
        #assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n        \include "_segments/segment--.ly"' in text
        assert '\n        \include "_segments/segment-A.ly"' in text
        assert '\n        \include "_segments/segment-B.ly"' in text


def test_AbjadIDE_generate_music_ly_02():
    """
    Comments out not-yet-extant segments.
    """

    with ide.Test():
        target = ide.Path('red_score', 'builds', 'letter-score', 'music.ly')
        target.remove()

        abjad_ide('red gg new C %letter ggc mlg q')
        transcript = abjad_ide.io.transcript
        assert f'Generating {target.trim()} ...' in transcript
        #assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n        \include "_segments/segment--.ly"' in text
        assert '\n        \include "_segments/segment-A.ly"' in text
        assert '\n        \include "_segments/segment-B.ly"' in text
        assert '\n        %\include "_segments/segment-C.ly"' in text
