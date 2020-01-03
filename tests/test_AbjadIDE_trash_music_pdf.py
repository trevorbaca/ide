import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_music_pdf_01():

    with ide.Test():
        path = ide.Path("red_score")
        path = path / "builds" / "letter-score" / "music.pdf"
        assert not path.exists()

        abjad_ide("red %let ggc mli q")
        assert path.is_file()

        abjad_ide("red %letter mpt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()
