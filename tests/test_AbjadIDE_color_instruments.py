import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_color_instruments_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score icl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring instruments ...",
            " Found 12 instrument color tags ...",
            " Activating 12 instrument color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score iuc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring instruments ...",
            " Found 12 instrument color tags ...",
            " Deactivating 12 instrument color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score icl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring instruments ...",
            " Found 12 instrument color tags ...",
            " Activating 12 instrument color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_instruments_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ icl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring instruments ...",
            " Found 16 instrument color tags ...",
            " Activating 4 instrument color tags ...",
            " Skipping 12 (active) instrument color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ iuc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring instruments ...",
            " Found 12 instrument color tags ...",
            " Deactivating 12 instrument color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ icl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring instruments ...",
            " Found 12 instrument color tags ...",
            " Activating 12 instrument color tags ...",
        ]:
            assert line in lines
