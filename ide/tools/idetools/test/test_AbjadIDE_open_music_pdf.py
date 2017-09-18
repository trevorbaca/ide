import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_music_pdf_01():

    abjad_ide('red~score %letter mo q')
    path = ide.Path('red_score').build('letter', 'music.pdf')
    transcript = abjad_ide.io.transcript
    assert f'Missing {path.trim()} ...' in transcript
