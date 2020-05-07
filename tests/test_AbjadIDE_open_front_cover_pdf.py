import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_front_cover_pdf_01():

    abjad_ide("red %letter fcpo q")
    transcript = abjad_ide.io.transcript
    assert f"No files matching front-cover.pdf ..." in transcript
