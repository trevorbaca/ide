import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_back_cover_pdf_01():

    abjad_ide("red bb letter bcpo q")
    transcript = abjad_ide.io.transcript
    assert "No files matching back-cover.pdf ..." in transcript
