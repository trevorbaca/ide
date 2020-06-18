import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_generate_stylesheet_ily_01():

    with ide.Test():
        directory = ide.configuration.boilerplate_directory
        source = abjad.Path(directory) / "stylesheet.ily"
        text = source.read_text()
        assert "paper_size" in text
        assert '"letter"' not in text
        target = abjad.Path(
            scores, "blue_score", "blue_score", "builds", "letter-score"
        )
        target /= "stylesheet.ily"
        target.remove()

        abjad_ide("blu bb letter ssig q")
        transcript = abjad_ide.io.transcript
        assert "Generating stylesheet ..." in transcript
        assert f"Removing {target.trim()} ..." not in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()
        text = target.read_text()
        assert "paper_size" not in text
        assert '"letter"' in text

        abjad_ide("blu bb letter ssig q")
        transcript = abjad_ide.io.transcript
        assert "Generating stylesheet ..." in transcript
        assert f"Removing {target.trim()} ..." in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()
        text = target.read_text()
        assert "paper_size" not in text
        assert '"letter"' in text
