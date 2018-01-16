import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_music_01():

    abjad_ide('red %letter mo q')
    path = ide.Path('red_score', 'builds', 'letter-score', 'music.pdf')
    transcript = abjad_ide.io.transcript
    assert f'No files matching music.pdf ...' in transcript
