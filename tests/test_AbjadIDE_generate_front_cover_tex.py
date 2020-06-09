import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_generate_front_cover_tex_01():

    with ide.Test():
        target = abjad.Path(scores, "red_score", "red_score", "builds", "letter-score")
        target /= "front-cover.tex"
        target.remove()

        abjad_ide("red bb letter fctg q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." not in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()

        abjad_ide("red bb letter fctg q")
        transcript = abjad_ide.io.transcript
        assert f"Removing {target.trim()} ..." in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()
