import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_every_pdf_01():
    r'''In materials directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').materials / 'magic_numbers'
        path /= 'illustration.pdf'

        abjad_ide('red~score %magic pdfm mm pdf* q')
        transcript = abjad_ide.io_manager.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_every_pdf_02():
    r'''In segments directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'

        abjad_ide('red~score %A pdfm gg pdf* q')
        transcript = abjad_ide.io_manager.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_every_pdf_03():
    r'''In scores directory.
    '''

    abjad_ide('pdf* q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').distribution / 'red-score.pdf'
    assert f'Opening {path.trim()} ...' in transcript
