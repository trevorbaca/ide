import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


tag = ide.tags.FIGURE_NAME


def test_AbjadIDE_show_figure_names_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score fns q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing FIGURE_NAME tags ...",
            " Found 1 FIGURE_NAME tag ...",
            " Activating 1 FIGURE_NAME tag ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score fnh q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding FIGURE_NAME tags ...",
            " Found 1 FIGURE_NAME tag ...",
            " Deactivating 1 FIGURE_NAME tag ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_figure_names_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ fnh q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding FIGURE_NAME tags ...",
            " Found 1 FIGURE_NAME tag ...",
            " Deactivating 1 FIGURE_NAME tag ...",
        ]:
            assert line in lines

        abjad_ide("gre _ fns q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing FIGURE_NAME tags ...",
            " Found 1 FIGURE_NAME tag ...",
            " Activating 1 FIGURE_NAME tag ...",
        ]:
            assert line in lines
