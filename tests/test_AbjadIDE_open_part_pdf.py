import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_open_part_pdf_01():

    with ide.Test():
        parts = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-parts")
        path = parts / "bass-clarinet" / "bass-clarinet-part.pdf"
        assert not parts.exists()
        assert not path.is_file()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y q")
        assert parts.exists()
        assert not path.is_file()

        path.write_text("")
        assert path.is_file()

        abjad_ide("gre bb arch-a-parts ppo bass q")
        transcript = abjad_ide.io.transcript
        assert f"Opening {path.trim()} ..." in transcript
