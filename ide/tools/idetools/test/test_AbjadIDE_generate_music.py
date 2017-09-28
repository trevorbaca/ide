import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_generate_music_01():

    with ide.Test():
        target = ide.Path('red_score', 'builds', 'letter', 'music.ly')
        target.remove()

        abjad_ide('red %letter mg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating music ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert 'Examining segments alphabetically ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/-.ly"' in text
        assert '\n    \include "../_segments/A.ly"' in text
        assert '\n    \include "../_segments/B.ly"' in text

        abjad_ide('red %letter mg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating music ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert 'Examining segments alphabetically ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/-.ly"' in text
        assert '\n    \include "../_segments/A.ly"' in text
        assert '\n    \include "../_segments/B.ly"' in text


def test_AbjadIDE_generate_music_02():
    r'''Comments out not-yet-extant segments.
    '''

    with ide.Test():
        target = ide.Path('red_score', 'builds', 'letter', 'music.ly')
        target.remove()

        abjad_ide('red gg new C %letter mg q')
        transcript = abjad_ide.io.transcript
        assert 'Generating music ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert 'Examining segments alphabetically ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/-.ly"' in text
        assert '\n    \include "../_segments/A.ly"' in text
        assert '\n    \include "../_segments/B.ly"' in text
        assert '\n    %\include "../_segments/C.ly"' in text
