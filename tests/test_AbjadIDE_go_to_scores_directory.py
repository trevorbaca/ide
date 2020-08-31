import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_scores_directory_01():
    """
    From segment directory.
    """

    abjad_ide("red gg 02 ss q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Abjad IDE : scores",
    ]


def test_AbjadIDE_go_to_scores_directory_02():
    """
    From score directory.
    """

    abjad_ide("red ss q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Abjad IDE : scores",
    ]


def test_AbjadIDE_go_to_scores_directory_03():
    """
    From home to home.
    """

    abjad_ide("ss q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == ["Abjad IDE : scores", "Abjad IDE : scores"]
