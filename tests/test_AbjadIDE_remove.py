import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_remove_01():
    """
    In build directory. Removes multiple files.
    """

    with ide.Test():
        path = ide.Path(scores, "red_score", "red_score", "builds", "letter-score")
        target_1 = path / "back-cover.tex"
        assert target_1.is_file()
        target_2 = path / "front-cover.tex"
        assert target_2.is_file()
        target_3 = path / "layout.ly"
        assert target_3.is_file()

        abjad_ide("red bb letter rm 1-3 remove~3 q")
        transcript = abjad_ide.io.transcript
        assert not target_1.exists()
        assert not target_2.exists()
        assert not target_3.exists()
        assert "Select files to remove> 1-3" in transcript
        assert "Will remove ..." in transcript
        assert f"    {target_1.trim()}" in transcript
        assert f"    {target_2.trim()}" in transcript
        assert f"    {target_3.trim()}" in transcript
        assert "Type 'remove 3' to proceed> remove 3" in transcript
        assert f"Removing {target_1.trim()} ..." in transcript
        assert f"Removing {target_2.trim()} ..." in transcript
        assert f"Removing {target_3.trim()} ..." in transcript

    with ide.Test():
        assert target_1.is_file()
        assert target_2.is_file()
        assert target_3.is_file()

        abjad_ide("red bb letter rm 2-1,3 remove~3 q")
        transcript = abjad_ide.io.transcript
        assert not target_1.exists()
        assert not target_2.exists()
        assert not target_3.exists()
        assert "Select files to remove> 2-1,3" in transcript
        assert "Will remove ..." in transcript
        assert f"    {target_2.trim()}" in transcript
        assert f"    {target_1.trim()}" in transcript
        assert f"    {target_3.trim()}" in transcript
        assert "Type 'remove 3' to proceed> remove 3" in transcript
        assert f"Removing {target_2.trim()} ..." in transcript
        assert f"Removing {target_1.trim()} ..." in transcript
        assert f"Removing {target_3.trim()} ..." in transcript

    with ide.Test():
        assert target_1.is_file()
        assert target_2.is_file()
        assert target_3.is_file()

        abjad_ide("red bb letter rm 2,1,3 remove~3 q")
        transcript = abjad_ide.io.transcript
        assert not target_1.exists()
        assert not target_2.exists()
        assert not target_3.exists()
        assert "Select files to remove> 2,1,3" in transcript
        assert "Will remove ..." in transcript
        assert f"    {target_2.trim()}" in transcript
        assert f"    {target_1.trim()}" in transcript
        assert f"    {target_3.trim()}" in transcript
        assert "Type 'remove 3' to proceed> remove 3" in transcript
        assert f"Removing {target_2.trim()} ..." in transcript
        assert f"Removing {target_1.trim()} ..." in transcript
        assert f"Removing {target_3.trim()} ..." in transcript


def test_AbjadIDE_remove_02():
    """
    In scores directory. Removes one package.
    """

    with ide.Test():
        path = ide.Path(scores, "blue_score")
        assert path.is_dir()

        abjad_ide("rm blu remove q")
        transcript = abjad_ide.io.transcript
        assert "Select packages to remove> blu" in transcript
        assert f"Will remove {path.trim()} ..."
        assert "Type 'remove' to proceed> remove" in transcript
        assert f"Removing {path.trim()} ..." in transcript
        assert not path.exists()


def test_AbjadIDE_remove_03():
    """
    In scores directory. Removes multiple packages.
    """

    with ide.Test():
        path_1 = ide.Path(scores, "blue_score")
        path_2 = ide.Path(scores, "red_score")

        abjad_ide("rm blu,red remove~2 q")
        for line in [
            "Select packages to remove> blu,red",
            "Will remove ...",
            f"    {path_1.trim()}",
            f"    {path_2.trim()}",
            "Type 'remove 2' to proceed> remove 2",
            f"Removing {path_1.trim()} ...",
            f"Removing {path_2.trim()} ...",
        ]:
            assert line in abjad_ide.io.transcript
        assert not path_1.exists()
        assert not path_2.exists()


def test_AbjadIDE_remove_04():
    """
    In stylesheets directory. Works with smart match.
    """

    with ide.Test():
        path = ide.Path(
            scores, "red_score", "red_score", "stylesheets", "stylesheet.ily"
        )

        abjad_ide("red yy rm sheet q")
        transcript = abjad_ide.io.transcript
        assert "Select files to remove> sheet" in transcript
        assert f"Will remove {path.trim()} ..." in transcript

        abjad_ide("red yy rm eet.i q")
        transcript = abjad_ide.io.transcript
        assert "Select files to remove> eet.i" in transcript
        assert f"Will remove {path.trim()} ..." in transcript

        abjad_ide("red yy rm sty q")
        transcript = abjad_ide.io.transcript
        assert "Select files to remove> sty" in transcript
        assert f"Will remove {path.trim()} ..." in transcript
