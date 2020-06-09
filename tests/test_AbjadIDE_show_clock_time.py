import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


tag = abjad.tags.CLOCK_TIME


def test_AbjadIDE_show_clock_time_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score cts q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing clock time markup ...",
            " Found 2 clock time markup tags ...",
            " Activating 2 clock time markup tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score cth q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding clock time markup ...",
            " Found 2 clock time markup tags ...",
            " Deactivating 2 clock time markup tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_clock_time_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ cts q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing clock time markup ...",
            " Found 2 clock time markup tags ...",
            " Activating 2 clock time markup tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ cth q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding clock time markup ...",
            " Found 2 clock time markup tags ...",
            " Deactivating 2 clock time markup tags ...",
        ]:
            assert line in lines
