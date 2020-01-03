import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_score_pdf_01():
    """
    Opens distribution score.
    """

    abjad_ide("red spo q")
    transcript = abjad_ide.io.transcript
    target = ide.Path("red_score", "distribution", "red-score.pdf")
    assert f"Opening {target.trim()} ..." in transcript


def test_AbjadIDE_open_score_pdf_02():
    """
    Opens build score.
    """

    abjad_ide("red %letter spo q")
    transcript = abjad_ide.io.transcript
    target = ide.Path("red_score", "builds", "letter-score", "score.pdf")
    assert f"No files ending in *score.pdf ..." in transcript


def test_AbjadIDE_open_score_pdf_03():

    abjad_ide("blu spo q")
    transcript = abjad_ide.io.transcript
    string = "Missing score PDF in distribution and build directories ..."
    assert string in transcript


def test_AbjadIDE_open_score_pdf_04():
    """
    In scores directory.
    """

    abjad_ide("spo q")
    transcript = abjad_ide.io.transcript
    target = ide.Path("red_score", "distribution", "red-score.pdf")
    assert f"Opening {target.trim()} ..." in transcript
