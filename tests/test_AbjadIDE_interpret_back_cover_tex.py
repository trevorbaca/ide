import ide
import os
import pytest

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_interpret_back_cover_tex_01():

    with ide.Test():
        source = ide.Path(
            "red_score", "builds", "letter-score", "back-cover.tex"
        )
        target = source.with_suffix(".pdf")
        target.remove()

        abjad_ide("red %letter bcti q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." not in transcript
        assert f"Interpreting {source.trim()} ..." in transcript
        assert f"Found {target.trim()} ..." in transcript
        assert f"Opening {target.trim()} ..." in transcript
        assert target.is_file()

        abjad_ide("red %letter bcti q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." in transcript
        assert f"Interpreting {source.trim()} ..." in transcript
        assert f"Found {target.trim()} ..." in transcript
        assert f"Opening {target.trim()} ..." in transcript
        assert target.is_file()
