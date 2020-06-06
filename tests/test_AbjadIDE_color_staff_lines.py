import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_color_staff_lines_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score slcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Activating 4 staff lines color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score sluc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Deactivating 4 staff lines color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score slcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Activating 4 staff lines color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_staff_lines_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre %_ slcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Skipping 4 (active) staff lines color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre %_ sluc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Deactivating 4 staff lines color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre %_ slcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Activating 4 staff lines color tags ...",
        ]:
            assert line in lines
