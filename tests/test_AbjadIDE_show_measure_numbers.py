import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_show_measure_numbers_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score mns q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing MEASURE_NUMBER tags ...",
            " Found 2 MEASURE_NUMBER tags ...",
            " Activating 2 MEASURE_NUMBER tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score mnh q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding MEASURE_NUMBER tags ...",
            " Found 2 MEASURE_NUMBER tags ...",
            " Deactivating 2 MEASURE_NUMBER tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_show_measure_numbers_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ mns q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Showing MEASURE_NUMBER tags ...",
            " Found 2 MEASURE_NUMBER tags ...",
            " Activating 2 MEASURE_NUMBER tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ mnh q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Hiding MEASURE_NUMBER tags ...",
            " Found 2 MEASURE_NUMBER tags ...",
            " Deactivating 2 MEASURE_NUMBER tags ...",
        ]:
            assert line in lines
