import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_materials_directory_01():
    """
    From builds directory.
    """

    abjad_ide("red bb mm q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Red Score (2017)",
        "Red Score (2017) : builds",
        "Red Score (2017) : materials",
    ]
    assert ".gitignore" not in transcript
