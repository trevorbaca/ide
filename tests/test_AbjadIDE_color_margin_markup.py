import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_color_margin_markup_01():
    """
    In build directory.
    """

    with ide.Test():

        build = abjad.Path(
            scores, "green_score", "green_score", "builds", "arch-a-score"
        )
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score mmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score mmuc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score mmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_margin_markup_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = abjad.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre _ mmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ mmuc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre _ mmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines
