import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_part_tex_01():

    with ide.Test():
        parts = abjad.Path(
            scores, "green_score", "green_score", "builds", "arch-a-parts"
        )
        assert not parts.exists()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y arch-a pte bass q")
        transcript = abjad_ide.io.transcript
        path = parts / "bass-clarinet" / "bass-clarinet-part.tex"
        assert f"Editing {path.trim()} ..." in transcript
