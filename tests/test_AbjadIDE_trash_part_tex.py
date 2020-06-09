import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_part_tex_01():

    with ide.Test():
        parts = abjad.Path(
            scores, "green_score", "green_score", "builds", "arch-a-parts"
        )
        path = parts / "bass-clarinet" / "bass-clarinet-part.tex"
        assert not parts.exists()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y q")
        assert path.is_file()

        abjad_ide("gre bb arch-a-parts ptt bass q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()
