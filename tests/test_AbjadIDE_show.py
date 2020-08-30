import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_show_01():
    """
    Shows clock time in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ show clock q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing CLOCK_TIME tags ...",
            " Found 2 CLOCK_TIME tags ...",
            " Activating 2 CLOCK_TIME tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ hide clock q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding CLOCK_TIME tags ...",
            " Found 2 CLOCK_TIME tags ...",
            " Deactivating 2 CLOCK_TIME tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_02():
    """
    Shows figure name in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ hide figure q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding FIGURE_NAME tags ...",
            " Found 1 FIGURE_NAME tag ...",
            " Deactivating 1 FIGURE_NAME tag ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ show figure q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing FIGURE_NAME tags ...",
            " Found 1 FIGURE_NAME tag ...",
            " Activating 1 FIGURE_NAME tag ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_03():
    """
    Show measure numbers in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ show measure q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing MEASURE_NUMBER tags ...",
            " Found 2 MEASURE_NUMBER tags ...",
            " Activating 2 MEASURE_NUMBER tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ hide measure q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding MEASURE_NUMBER tags ...",
            " Found 2 MEASURE_NUMBER tags ...",
            " Deactivating 2 MEASURE_NUMBER tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_04():
    """
    Shows spacing in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "layout.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ show spacing q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing spacing tags ...",
            " Found 2 spacing tags ...",
            " Activating 2 spacing tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ hide spacing q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding spacing tags ...",
            " Found 2 spacing tags ...",
            " Deactivating 2 spacing tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_05():
    """
    Shows stage numbers in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ show stage q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing STAGE_NUMBER tags ...",
            " Found 2 STAGE_NUMBER tags ...",
            " Activating 2 STAGE_NUMBER tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ hide stage q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding STAGE_NUMBER tags ...",
            " Found 2 STAGE_NUMBER tags ...",
            " Deactivating 2 STAGE_NUMBER tags ...",
        ]:
            assert line in lines
