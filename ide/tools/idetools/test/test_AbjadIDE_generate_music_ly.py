import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_music_ly_01():

    with ide.Test():
        target = ide.Path('red_score').build / 'letter' / 'music.ly'
        target.remove()

        input_ = 'red~score %letter mg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating music ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert 'Examining segments in alphabetical order ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
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
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating music ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert 'Examining segments in alphabetical order ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
        text = target.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\version' in text
        assert r'\language' in text
        assert '\n    \include "../_segments/segment-01.ly"' in text
        assert '\n    \include "../_segments/segment-02.ly"' in text
        assert '\n    \include "../_segments/segment-03.ly"' in text
