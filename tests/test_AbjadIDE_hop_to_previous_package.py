import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_hop_to_previous_package_01():
    """
    In segments directory.
    """

    abjad_ide("red gg < < < q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 03",
        "Red Score (2017) : segments : 02",
        "Red Score (2017) : segments : 01",
    ]


def test_AbjadIDE_hop_to_previous_package_02():
    """
    In segment directory.
    """

    abjad_ide("red gg 01 < < q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : segments",
        "Red Score (2017) : segments : 01",
        "Red Score (2017) : segments : 03",
        "Red Score (2017) : segments : 02",
    ]
