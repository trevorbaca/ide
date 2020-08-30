import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_color_01():
    """
    Colors clefs in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring clefs ...",
            " Found 14 clef color tags ...",
            " Skipping 14 (active) clef color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring clefs ...",
            " Found 14 clef color tags ...",
            " Deactivating 14 clef color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color clefs q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring clefs ...",
            " Found 14 clef color tags ...",
            " Activating 14 clef color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_02():
    """
    Colors dynamics in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color dynamics q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring dynamics ...",
            " Found 2 dynamic color tags ...",
            " Skipping 2 (active) dynamic color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor dynamics q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring dynamics ...",
            " Found 2 dynamic color tags ...",
            " Deactivating 2 dynamic color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color dynamics q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring dynamics ...",
            " Found 2 dynamic color tags ...",
            " Activating 2 dynamic color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_03():
    """
    Colors instruments in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color instruments q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring instruments ...",
            " Found 16 instrument color tags ...",
            " Activating 4 instrument color tags ...",
            " Skipping 12 (active) instrument color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor instruments q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring instruments ...",
            " Found 12 instrument color tags ...",
            " Deactivating 12 instrument color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color instruments q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring instruments ...",
            " Found 12 instrument color tags ...",
            " Activating 12 instrument color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_04():
    """
    Colors margin markup in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color margin q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor margin q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color margin q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring margin markup ...",
            " Found no margin markup color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_05():
    """
    Colors metronoms marks in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color metronome q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring metronome marks ...",
            " Found 1 metronome mark color expression tag ...",
            " Skipping 1 (active) metronome mark color expression tag ...",
            " Found 1 metronome mark color suppression tag ...",
            " Skipping 1 (inactive) metronome mark color suppression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor metro q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring metronome marks ...",
            " Found 1 metronome mark color suppression tag ...",
            " Activating 1 metronome mark color suppression tag ...",
            " Found 1 metronome mark color expression tag ...",
            " Deactivating 1 metronome mark color expression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color metronome q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring metronome marks ...",
            " Found 1 metronome mark color expression tag ...",
            " Activating 1 metronome mark color expression tag ...",
            " Found 1 metronome mark color suppression tag ...",
            " Deactivating 1 metronome mark color suppression tag ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_06():
    """
    Colors persistent indicators in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color persistent q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring persistent indicators ...",
            " Found 30 persistent indicator color expression tags ...",
            " Activating 4 persistent indicator color expression tags ...",
            " Skipping 26 (active) persistent indicator color expression tags ...",
            " Found 1 persistent indicator color suppression tag ...",
            " Skipping 1 (inactive) persistent indicator color suppression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor persistent q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring persistent indicators ...",
            " Found 26 persistent indicator color expression tags ...",
            " Deactivating 26 persistent indicator color expression tags ...",
            " Found 1 persistent indicator color suppression tag ...",
            " Activating 1 persistent indicator color suppression tag ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color persistent q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring persistent indicators ...",
            " Found 26 persistent indicator color expression tags ...",
            " Activating 26 persistent indicator color expression tags ...",
            " Found 1 persistent indicator color suppression tag ...",
            " Deactivating 1 persistent indicator color suppression tag ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_07():
    """
    Colors staff lines in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color staff q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Skipping 4 (active) staff lines color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor staff q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Deactivating 4 staff lines color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color staff q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring staff lines ...",
            " Found 4 staff lines color tags ...",
            " Activating 4 staff lines color tags ...",
        ]:
            assert line in lines


def test_AbjadIDE_color_08():
    """
    Colors time signatures in segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "green_score", "green_score", "segments", "_", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("gre gg _ color time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Skipping 2 (active) time signature color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ uncolor time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Uncoloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Deactivating 2 time signature color tags ...",
        ]:
            assert line in lines

        abjad_ide("gre gg _ color time q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Coloring time signatures ...",
            " Found 2 time signature color tags ...",
            " Activating 2 time signature color tags ...",
        ]:
            assert line in lines
