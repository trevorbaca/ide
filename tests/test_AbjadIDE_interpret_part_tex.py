import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_interpret_part_tex_01():

    with ide.Test():
        parts = ide.Path(scores, "green_score", "green_score", "builds", "arch-a-parts")
        part_directory = parts / "bass-clarinet"
        part_tex = part_directory / "bass-clarinet-part.tex"
        part_pdf = part_tex.with_suffix(".pdf")
        assert not parts.exists()
        assert not part_tex.exists()
        assert not part_pdf.exists()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y q")
        assert parts.exists()
        assert part_tex.is_file()
        assert not part_pdf.exists()

        for name in [
            "bass-clarinet-front-cover.pdf",
            "bass-clarinet-preface.pdf",
            "bass-clarinet-music.pdf",
            "bass-clarinet-back-cover.pdf",
        ]:
            abjad_ide._copy_boilerplate(part_directory, "blank.pdf", target_name=name)

        abjad_ide("gre bb arch pti bass q")
        transcript = abjad_ide.io.transcript
        assert f"Interpreting {part_tex.trim()} ..." in transcript
        assert parts.exists()
        assert part_directory.exists()
        assert part_tex.is_file()
        assert part_pdf.is_file()
