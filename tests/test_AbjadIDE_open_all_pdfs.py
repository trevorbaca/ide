import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_open_all_pdfs_01():

    for name in ["_", "A", "B"]:
        path = ide.Path(
            scores, "red_score", "red_score", "segments", name, "illustration.pdf"
        )
        path.remove()

    with ide.Test():
        path = ide.Path(
            scores, "red_score", "red_score", "segments", "_", "illustration.pdf"
        )

        abjad_ide("red %_ ipm q")
        assert path.is_file()

        abjad_ide("red gg ** q")
        transcript = abjad_ide.io.transcript
        assert "Matching '**' to 1 file ..." in transcript
        assert f"Opening {path.trim()} ..." in transcript

        abjad_ide("red gg **0 q")
        transcript = abjad_ide.io.transcript
        assert "Matching '**0' to 0 files ..." in transcript

        abjad_ide("red gg **1 q")
        transcript = abjad_ide.io.transcript
        assert "Matching '**1' to 0 files ..." in transcript

        abjad_ide("red gg **99 q")
        transcript = abjad_ide.io.transcript
        assert "Matching '**99' to 0 files ..." in transcript
