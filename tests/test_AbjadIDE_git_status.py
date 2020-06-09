import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_git_status_01():
    """
    In score directories.
    """

    abjad_ide("red st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript

    abjad_ide("red bb st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript

    abjad_ide("red dd st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript

    abjad_ide("red ee st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript

    abjad_ide("red gg st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript

    abjad_ide("red gg A st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript

    abjad_ide("red yy st q")
    transcript = abjad_ide.io.transcript
    assert "Running git status . ..." in transcript
    assert "Running git submodule foreach git fetch ..." in transcript


def test_AbjadIDE_git_status_02():
    """
    In scores directory.
    """

    abjad_ide("st q")
    transcript = abjad_ide.io.transcript
    for path in [abjad.Path(scores, "red_score"), abjad.Path(scores, "blue_score")]:
        assert f"{path} ..." in transcript
        assert "Running git status . ..." in transcript
        assert "Running git submodule foreach git fetch ..." in transcript
