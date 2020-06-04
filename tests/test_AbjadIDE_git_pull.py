import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_pull_01():
    """
    In score directories.
    """

    abjad_ide("red pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red bb pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red dd pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red ee pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red gg pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red gg A pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red tt pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript

    abjad_ide("red yy pull q")
    transcript = abjad_ide.io.transcript
    assert "Running git pull ..." in transcript


def test_AbjadIDE_git_pull_02():
    """
    In scores directory.
    """

    abjad_ide("pull q")
    transcript = abjad_ide.io.transcript
    for path in [ide.Path("red_score"), ide.Path("blue_score")]:
        assert f"{path.wrapper} ..." in transcript
        assert "Running git pull ..." in transcript
