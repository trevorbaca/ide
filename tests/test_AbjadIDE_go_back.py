import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_back_01():

    abjad_ide("red gg 02 bb - - q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : builds",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : builds",
    ]


def test_AbjadIDE_go_back_02():

    abjad_ide("red - - - q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Abjad IDE : scores",
    ]


def test_AbjadIDE_go_back_03():
    """
    Regression: back manages scores directory rather than quitting.
    """

    abjad_ide("- q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == ["Abjad IDE : scores", "Abjad IDE : scores"]
