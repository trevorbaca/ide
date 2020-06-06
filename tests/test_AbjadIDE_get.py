import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_get_01():
    """
    In build directory.
    """

    with ide.Test():
        source = ide.Path(scores, "red_score", "red_score", "builds", "letter-score")
        source /= "front-cover.tex"
        assert source.is_file()
        target = source.with_score("blue_score")
        target.remove()

        abjad_ide("blu %letter get red ont-co y q")
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        header = "Blue Score (2017) : builds : letter-score (empty)"
        header += " : get files from ..."
        assert header in transcript
        assert header in transcript
        header = "Blue Score (2017) : distribution (empty)"
        header += " : get Red Score (2017) files ..."
        assert "> red" in transcript
        assert f"Getting {source.trim()} ..." in transcript
        assert f"Will write {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert f"Writing {target.trim()} ..." in transcript


def test_AbjadIDE_get_02():
    """
    In distribution directory.
    """

    with ide.Test():
        source = ide.Path(
            scores, "red_score", "red_score", "distribution", "red-score.pdf"
        )
        assert source.is_file()
        target = source.with_score("blue_score")
        target.remove()

        abjad_ide("blu dd get red ore.pdf y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = "Blue Score (2017) : distribution (empty)"
        header += " : get files from ..."
        assert header in transcript
        header = "Blue Score (2017) : distribution (empty)"
        header += " : get Red Score (2017) files ..."
        assert header in transcript
        assert "> red" in transcript
        assert "> ore.pdf" in transcript
        assert f"Getting {source.trim()} ..." in transcript
        assert f"Will write {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert f"Writing {target.trim()} ..." in transcript


def test_AbjadIDE_get_03():
    """
    In etc directory.
    """

    with ide.Test():
        source = ide.Path(scores, "red_score", "red_score", "etc", "notes.txt")
        assert source.is_file()
        target = source.with_score("blue_score")
        target.remove()

        abjad_ide("blu ee get red otes.txt y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = "Blue Score (2017) : etc (empty) : get files from ..."
        assert header in transcript
        header = "Blue Score (2017) : etc (empty)"
        header += " : get Red Score (2017) files ..."
        assert header in transcript
        assert "> red" in transcript
        assert "> otes.txt" in transcript
        assert f"Getting {source.trim()} ..." in transcript
        assert f"Will write {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert f"Writing {target.trim()} ..." in transcript


def test_AbjadIDE_get_04():
    """
    In segment directory.
    """

    with ide.Test():
        source = ide.Path(
            scores, "red_score", "red_score", "segments", "A", "definition.py"
        )
        assert source.is_file()
        target = source.with_parent("B")
        target.remove()

        abjad_ide("red %B get A y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = "Red Score (2017) : segments : B : get file ..."
        assert header in transcript
        assert "> A" in transcript
        assert f"Getting {source.trim()} ..." in transcript
        assert f"Will write {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert f"Writing {target.trim()} ..." in transcript

    # regression: return jumps from selector
    abjad_ide("blu %_ get <return> q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Blue Score (2017)",
        "Blue Score (2017) : segments : _",
        "Blue Score (2017) : segments : _ : get file ...",
        "Blue Score (2017) : segments : _",
    ]

    # regression: quit jumps from selector
    abjad_ide("blu %_ get q")
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        "Abjad IDE : scores",
        "Blue Score (2017)",
        "Blue Score (2017) : segments : _",
        "Blue Score (2017) : segments : _ : get file ...",
    ]
    assert "Matches no file 'q' ..." not in transcript


def test_AbjadIDE_get_05():
    """
    In segments directory.
    """

    with ide.Test():
        source = ide.Path(scores, "red_score", "red_score", "segments", "B")
        assert source.is_dir()
        target = source.with_score("blue_score")
        target.remove()

        abjad_ide("blu gg get red B y <return> q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = "Blue Score (2017) : segments : get packages from ..."
        assert header in transcript
        header = "Blue Score (2017) : segments"
        header += " : get Red Score (2017) packages ..."
        assert header in transcript
        assert "> red" in transcript
        assert "> B" in transcript
        assert f"Getting {source.trim()} ..." in transcript
        assert f"Will write {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert f"Writing {target.trim()} ..." in transcript


def test_AbjadIDE_get_06():
    """
    In stylesheets directory.
    """

    with ide.Test():
        source = ide.Path(
            scores, "red_score", "red_score", "stylesheets", "stylesheet.ily"
        )
        assert source.is_file()
        target = source.with_score("blue_score")
        target.remove()

        abjad_ide("blu yy get red eet.i y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = "Blue Score (2017) : stylesheets (empty) : get files from ..."
        assert header in transcript
        assert "> red" in transcript
        assert "> eet.i" in transcript
        assert f"Getting {source.trim()} ..." in transcript
        assert f"Will write {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert f"Writing {target.trim()} ..." in transcript
