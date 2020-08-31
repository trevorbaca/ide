import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_builds_directory_01():
    """
    From segment directory.
    """

    abjad_ide("red gg 02 bb q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : builds",
    ]


def test_AbjadIDE_go_to_builds_directory_02():
    """
    From score directory.
    """

    abjad_ide("red dd q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : distribution",
    ]


def test_AbjadIDE_go_to_builds_directory_03():
    """
    From builds directory to builds directory.
    """

    abjad_ide("red bb bb q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : builds",
        "Red Score (2017) : builds",
    ]


def test_AbjadIDE_go_to_builds_directory_04():
    """
    Git ignore file is hidden.
    """

    abjad_ide("red bb q")
    transcript = abjad_ide.io.transcript
    assert ".gitignore" not in transcript
