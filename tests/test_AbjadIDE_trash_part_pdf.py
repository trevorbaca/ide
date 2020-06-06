import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_part_pdf_01():

    with ide.Test():
        parts = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-parts")
        path = parts / "bass-clarinet" / "bass-clarinet-part.pdf"
        assert not parts.exists()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y q")
        assert parts.exists()

        path.write_text("")
        assert path.is_file()

        abjad_ide("gre bb arch-a-parts ppt bass q")
        transcript = abjad_ide.io.transcript
        assert not path.exists()
        assert f"Trashing {path.trim()} ..." in transcript
