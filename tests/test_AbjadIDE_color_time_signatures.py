import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_color_time_signatures_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score color time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Activating 2 time signature color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score uncolor time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Deactivating 2 time signature color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score color time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Activating 2 time signature color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_time_signatures_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ color time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Skipping 2 (active) time signature color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ uncolor time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Deactivating 2 time signature color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ color time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Activating 2 time signature color tags ...",
        ]:
            assert line in lines
