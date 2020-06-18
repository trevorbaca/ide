import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_rename_01():
    """
    Renames score package.
    """

    with ide.Test():
        source = abjad.Path(scores, "blue_score", "blue_score")
        assert source.is_dir()
        target = ide.configuration.test_scores_directory / "purple_score"
        target.remove()

        abjad_ide("ren blu Purple~Score y q")
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_02():
    """
    Renames segment directory.
    """

    with ide.Test():
        source = abjad.Path(scores, "red_score", "red_score", "segments", "D")
        source.remove()
        target = source.with_name("E")
        target.remove()

        abjad_ide("red gg new D q")
        assert source.is_dir()

        abjad_ide("red gg ren D E y q")
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert "Select packages to rename> D" in transcript
        assert f"Renaming {source.trim()} ..." in transcript
        assert "New name> E" in transcript
        assert "Renaming ..." in transcript
        assert f" FROM: {source.trim()}" in transcript
        assert f"   TO: {target.trim()}" in transcript
        assert "Ok?> y" in transcript


def test_AbjadIDE_rename_03():
    """
    Renames named segment.
    """

    with ide.Test():
        source = abjad.Path(scores, "red_score", "red_score", "segments", "B")
        assert source.is_dir()
        target = source.with_name("C")
        target.remove()

        abjad_ide("red gg ren B C y q")
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert "Select packages to rename> B" in transcript
        assert f"Renaming {source.trim()} ..." in transcript
        assert "New name> C" in transcript
        assert "Renaming ..." in transcript
        assert f" FROM: {source.trim()}" in transcript
        assert f"   TO: {target.trim()}" in transcript
        assert "Ok?> y" in transcript


def test_AbjadIDE_rename_04():
    """
    Renames build directory.
    """

    with ide.Test():
        source = abjad.Path(scores, "red_score", "red_score", "builds", "letter-score")
        assert source.is_dir()
        target = source.with_name("standard-size")
        target.remove()

        abjad_ide("red bb ren letter standard~size y q")
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert "Select directories to rename> letter" in transcript
        assert f"Renaming {source.trim()} ..." in transcript
        assert "New name> standard size" in transcript
        assert "Renaming ..." in transcript
        assert f" FROM: {source.trim()}" in transcript
        assert f"   TO: {target.trim()}" in transcript
        assert "Ok?> y" in transcript


def test_AbjadIDE_rename_05():
    """
    Renames stylesheet.
    """

    with ide.Test():
        source = abjad.Path(
            scores, "red_score", "red_score", "stylesheets", "new-stylesheet.ily"
        )
        source.remove()
        target = source.with_name("renamed-stylesheet.ily")
        target.remove()

        abjad_ide("red yy new new-stylesheet.ily y q")
        assert source.is_file()

        abjad_ide("red yy ren new- renamed-stylesheet y q")
        assert not source.exists()
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_file()
        assert "Select files to rename> new-" in transcript
        assert f"Renaming {source.trim()} ..." in transcript
        assert "New name> renamed-stylesheet" in transcript
        assert "Renaming ..." in transcript
        assert f" FROM: {source.trim()}" in transcript
        assert f"   TO: {target.trim()}" in transcript
        assert "Ok?> y" in transcript
