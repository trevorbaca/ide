import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_duplicate_01():
    """
    In build directory.
    """

    abjad_ide("red bb let dup layout.ly q")
    transcript = abjad_ide.io.transcript
    assert "Select files to duplicate> layout.ly" in transcript
    assert "Duplicating red_score/builds/letter-score/layout.ly ..." in transcript
    assert "Enter new name> q" in transcript


def test_AbjadIDE_duplicate_02():
    """
    In distribution directory.
    """

    abjad_ide("red dd dup red-score.pdf q")
    transcript = abjad_ide.io.transcript
    assert "Select files to duplicate> red-score.pdf" in transcript
    assert "Duplicating red_score/distribution/red-score.pdf ..." in transcript
    assert "Enter new name> q" in transcript


def test_AbjadIDE_duplicate_03():
    """
    In etc directory.
    """

    abjad_ide("red ee dup notes.txt q")
    transcript = abjad_ide.io.transcript
    assert "Select files to duplicate> notes.txt" in transcript
    assert "Duplicating red_score/etc/notes.txt ..." in transcript
    assert "Enter new name> q" in transcript


def test_AbjadIDE_duplicate_04():
    """
    In scores directory.
    """

    with ide.Test():
        source = abjad.Path(scores, "red_score")
        assert source.is_dir()
        target = source.with_name("purple_score")
        target.remove()

        abjad_ide("dup red Purple~Score y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert "Select packages to duplicate> red" in transcript
        assert f"Duplicating {source.trim()} ..." in transcript
        assert "Enter title> Purple Score" in transcript
        assert "Ok?> y" in transcript
        assert "Replacing 'red_score' with 'purple_score' ..." in transcript
        assert "Replacing 'Red Score' with 'Purple Score' ..." in transcript


def test_AbjadIDE_duplicate_05():
    """
    In scores directory. Handles empty return gracefully.
    """

    abjad_ide("dup <return> q")
    transcript = abjad_ide.io.transcript
    assert "Select packages to duplicate> " in transcript


def test_AbjadIDE_duplicate_06():
    """
    In segments directory.
    """

    with ide.Test():
        source = abjad.Path(scores, "blue_score", "blue_score", "segments", "A")
        assert source.is_dir()
        target = source.with_name("B")
        target.remove()

        abjad_ide("blu gg dup A B y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert "Select packages to duplicate> A" in transcript
        assert f"Duplicating {source.trim()} ..."
        assert "Enter new name> B"
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert "Replacing 'A' with 'B' ..." in transcript


def test_AbjadIDE_duplicate_07():
    """
    In stylesheets directory.
    """

    with ide.Test():
        source = abjad.Path(
            scores, "red_score", "red_score", "stylesheets", "stylesheet.ily"
        )
        assert source.is_file()
        target = source.with_name("new-stylesheet.ily")
        target.remove()

        abjad_ide("red yy dup eet.i new~stylesheet y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert "Select files to duplicate> eet.i" in transcript
        assert f"Duplicating {source.trim()} ..." in transcript
        assert "Enter new name> new stylesheet" in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
