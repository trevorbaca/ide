import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_music_pdf_01():

    with ide.Test():
        path = ide.Path(scores, "red_score", "red_score")
        path = path / "builds" / "letter-score" / "music.pdf"
        assert not path.exists()

        abjad_ide("red bb let ggc mli q")
        assert path.is_file()

        abjad_ide("red bb letter mpt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()
