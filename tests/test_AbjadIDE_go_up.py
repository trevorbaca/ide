import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_up_01():

    abjad_ide("red gg 02 .. .. .. q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : segments",
        "Red Score (2017)",
        "Red Score (2017) : wrapper",
    ]
