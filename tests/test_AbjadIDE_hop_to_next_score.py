import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_hop_to_next_score_01():
    """
    In scores directory.
    """

    abjad_ide(">> >> >> q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Blue Score (2017)",
        "Green Score (2018)",
        "Red Score (2017)",
    ]
