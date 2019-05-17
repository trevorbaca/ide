import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_distribution_directory_01():
    """
    From material directory.
    """

    abjad_ide("red mm metronome dd q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : materials",
        "Red Score (2017) : materials : metronome_marks",
        "Red Score (2017) : distribution",
    ]
    assert ".gitignore" in transcript


def test_AbjadIDE_go_to_distribution_directory_02():
    """
    From segment directory.
    """

    abjad_ide("red gg A dd q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : A",
        "Red Score (2017) : distribution",
    ]


def test_AbjadIDE_go_to_distribution_directory_03():
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


def test_AbjadIDE_go_to_distribution_directory_04():
    """
    From builds directory to distribution directory.
    """

    abjad_ide("red bb dd q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : builds",
        "Red Score (2017) : distribution",
    ]
