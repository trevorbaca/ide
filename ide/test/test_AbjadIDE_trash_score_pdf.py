import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_score_pdf_01():

    with ide.Test():
        path = ide.Path('red_score')
        path = path / 'builds' / 'letter-score' / 'score.pdf'
        assert not path.exists()

        path.write_text('')
        assert path.is_file()

        abjad_ide('red %let spt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()
