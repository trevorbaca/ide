import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_show_spacing_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score sps q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing spacing tags ...",
            " Found no spacing tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_spacing_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "layout.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ sps q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing spacing tags ...",
            " Found 2 spacing tags ...",
            " Activating 2 spacing tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ sph q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding spacing tags ...",
            " Found 2 spacing tags ...",
            " Deactivating 2 spacing tags ...",
        ]:
            assert line in lines
