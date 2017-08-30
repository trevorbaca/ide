import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_music_ly_01():

    with ide.Test():
        target = ide.PackagePath('red_score').builds / 'letter' / 'music.ly'
        target.remove()

        input_ = 'red~score %letter mg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating music ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert 'Examining segments alphabetically ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/segment-01.ly"' in text
        assert '\n    \include "../_segments/segment-02.ly"' in text
        assert '\n    \include "../_segments/segment-03.ly"' in text

        input_ = 'red~score %letter mg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating music ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert 'Examining segments alphabetically ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/segment-01.ly"' in text
        assert '\n    \include "../_segments/segment-02.ly"' in text
        assert '\n    \include "../_segments/segment-03.ly"' in text


def test_AbjadIDE_generate_music_ly_02():
    r'''Comments out not-yet-extant segments.
    '''

    with ide.Test():
        target = ide.PackagePath('red_score').builds / 'letter' / 'music.ly'
        target.remove()

        input_ = 'red~score gg new segment~04 %letter mg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating music ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert 'Examining segments alphabetically ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/segment-01.ly"' in text
        assert '\n    \include "../_segments/segment-02.ly"' in text
        assert '\n    \include "../_segments/segment-03.ly"' in text
        assert '\n    %\include "../_segments/segment-04.ly"' in text
