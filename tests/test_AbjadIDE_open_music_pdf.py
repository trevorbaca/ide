import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_music_pdf_01():

    abjad_ide("red %letter mpo q")
    transcript = abjad_ide.io.transcript
    assert "No files matching music.pdf ..." in transcript
