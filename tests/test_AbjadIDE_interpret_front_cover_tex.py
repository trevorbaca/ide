import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_interpret_front_cover_tex_01():

    with ide.Test():
        source = ide.Path(
            scores,
            "red_score",
            "red_score",
            "builds",
            "letter-score",
            "front-cover.tex",
        )
        target = source.with_suffix(".pdf")
        target.remove()

        abjad_ide("red %letter fcti q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." not in transcript
        assert f"Interpreting {source.trim()} ..." in transcript
        assert f"Found {target.trim()} ..." in transcript
        assert f"Opening {target.trim()} ..." in transcript
        assert target.is_file()

        abjad_ide("red %letter fcti q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." in transcript
        assert f"Interpreting {source.trim()} ..." in transcript
        assert f"Found {target.trim()} ..." in transcript
        assert f"Opening {target.trim()} ..." in transcript
        assert target.is_file()
