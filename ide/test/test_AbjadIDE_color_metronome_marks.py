import abjad
import baca
import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_metronome_marks_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path("green_score", "builds", "arch-a-score")
        path = build / "_segments" / "segment--.ly"

        abjad_ide("gre bb arch-a-score ggc q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-score tmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring metronome marks ...",
            " Found 1 metronome mark color expression tag ...",
            " Activating 1 metronome mark color expression tag ...",
            " Found 1 metronome mark color suppression tag ...",
            " Deactivating 1 metronome mark color suppression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score tmuc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring metronome marks ...",
            " Found 1 metronome mark color suppression tag ...",
            " Activating 1 metronome mark color suppression tag ...",
            " Found 1 metronome mark color expression tag ...",
            " Deactivating 1 metronome mark color expression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre bb arch-a-score tmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring metronome marks ...",
            " Found 1 metronome mark color expression tag ...",
            " Activating 1 metronome mark color expression tag ...",
            " Found 1 metronome mark color suppression tag ...",
            " Deactivating 1 metronome mark color suppression tag ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_metronome_marks_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path("green_score", "segments", "_", "illustration.ly")
        assert path.is_file()

        abjad_ide("gre %_ tmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring metronome marks ...",
            " Found 1 metronome mark color expression tag ...",
            " Skipping 1 (active) metronome mark color expression tag ...",
            " Found 1 metronome mark color suppression tag ...",
            " Skipping 1 (inactive) metronome mark color suppression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre %_ tmuc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring metronome marks ...",
            " Found 1 metronome mark color suppression tag ...",
            " Activating 1 metronome mark color suppression tag ...",
            " Found 1 metronome mark color expression tag ...",
            " Deactivating 1 metronome mark color expression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre %_ tmcl q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring metronome marks ...",
            " Found 1 metronome mark color expression tag ...",
            " Activating 1 metronome mark color expression tag ...",
            " Found 1 metronome mark color suppression tag ...",
            " Deactivating 1 metronome mark color suppression tag ...",
        ]:
            assert line in lines
