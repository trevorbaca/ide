import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_contents_directory_01():
    """
    From builds directory.
    """

    abjad_ide("red bb cc q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : builds",
        "Red Score (2017)",
    ]


def test_AbjadIDE_go_to_contents_directory_02():
    """
    From interrupted getter.
    """

    abjad_ide("red bb new cc q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : builds",
        "Red Score (2017)",
    ]


def test_AbjadIDE_go_to_contents_directory_03():
    """
    From score directory.
    """

    abjad_ide("red cc q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017)",
    ]


def test_AbjadIDE_go_to_contents_directory_04():
    """
    From scores directory.
    """

    abjad_ide("lue q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == ["Abjad IDE : scores", "Blue Score (2017)"]

    abjad_ide("BSc q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == ["Abjad IDE : scores", "Blue Score (2017)"]


def test_AbjadIDE_go_to_contents_directory_05():
    """
    From segment directory.
    """

    abjad_ide("red gg 02 cc q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 02",
        "Red Score (2017)",
    ]
