import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_segments_directory_01():
    """
    From segment directory.
    """

    abjad_ide("red gg 02 gg q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : segments",
    ]


def test_AbjadIDE_go_to_segments_directory_02():
    """
    From score directory.
    """

    abjad_ide("red gg q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
    ]
