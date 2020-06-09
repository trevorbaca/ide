import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_generate_preface_tex_01():

    with ide.Test():
        directory = abjad.abjad_configuration.boilerplate_directory
        source = abjad.Path(directory) / "score-preface.tex"
        text = source.read_text()
        assert "paper_size" in text
        assert "{8.5in, 11in}" not in text
        target = abjad.Path(
            scores, "blue_score", "blue_score", "builds", "letter-score"
        )
        target /= "preface.tex"
        target.remove()

        abjad_ide("blu bb letter pftg q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." not in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()
        text = target.read_text()
        assert "paper_size" not in text
        assert "{8.5in, 11in}" in text

        abjad_ide("blu bb letter pftg q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()
        text = target.read_text()
        assert "paper_size" not in text
        assert "{8.5in, 11in}" in text
