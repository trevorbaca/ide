import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_part_tex_01():

    with ide.Test():
        parts = ide.Path("green_score", "builds", "arch-a-parts")
        assert not parts.exists()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y arch-a pte bass q")
        transcript = abjad_ide.io.transcript
        path = parts / "bass-clarinet" / "bass-clarinet-part.tex"
        assert f"Editing {path.trim()} ..." in transcript
