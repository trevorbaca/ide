import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_back_cover_pdf_01():

    with ide.Test():
        path = ide.Path(scores, "red_score", "red_score")
        path = path / "builds" / "letter-score" / "back-cover.pdf"
        assert not path.exists()

        path.write_text("")
        assert path.is_file()

        abjad_ide("red %letter bcpt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()
