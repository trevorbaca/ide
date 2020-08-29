import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_color_clefs_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score color clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring clefs ...",
            " Found 14 clef color tags ...",
            " Activating 14 clef color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score uncolor clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring clefs ...",
            " Found 14 clef color tags ...",
            " Deactivating 14 clef color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score color clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring clefs ...",
            " Found 14 clef color tags ...",
            " Activating 14 clef color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_clefs_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ color clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring clefs ...",
            " Found 14 clef color tags ...",
            " Skipping 14 (active) clef color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ uncolor clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring clefs ...",
            " Found 14 clef color tags ...",
            " Deactivating 14 clef color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ color clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring clefs ...",
            " Found 14 clef color tags ...",
            " Activating 14 clef color tags ...",
        ]:
            assert line in lines
