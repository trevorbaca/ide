import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_wrapper_directory_01():
    """
    From segment directory.
    """

    abjad_ide("red gg 02 ww q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : wrapper",
    ]


def test_AbjadIDE_go_to_wrapper_directory_02():
    """
    From builds directory.
    """

    abjad_ide("red bb ww q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : builds",
        "Red Score (2017) : wrapper",
    ]
