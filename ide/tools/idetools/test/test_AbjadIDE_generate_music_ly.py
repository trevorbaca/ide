import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_music_ly_01():
    r'''When music does not exist yet.

    Can't use filecmp because music.ly file contains LilyPond version
    directive, LilyPond language directive and file paths.
    '''

    with ide.Test():
        path = ide.Path('red_score').build / 'letter' / 'music.ly'
        path.unlink()
        input_ = 'red~score bb letter mg q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'Red Score (2017) for piano' in text
        assert r'\language' in text
        assert r'\version' in text
        # indent include statements exactly four spaces
        assert '\n' + 4 * ' ' + r'\include' in text
