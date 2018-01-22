import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_preface_pdf_01():

    with ide.Test():
        path = ide.Path('red_score')
        path = path('builds', 'letter-score', 'preface.pdf')
        assert not path.exists()

        abjad_ide('red %let pi q')
        assert path.is_file()

        abjad_ide('red %let ppt q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()
