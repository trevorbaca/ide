import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_every_pdf_01():
    r'''In materials directory.
    '''

    with ide.Test():
        path = ide.PackagePath('red_score').materials / 'magic_numbers'
        path /= 'illustration.pdf'

        input_ = 'red~score %magic~numbers pdfm mm pdf* q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_every_pdf_02():
    r'''In segments directory.
    '''

    with ide.Test():
        path = ide.PackagePath('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'
        input_ = 'red~score %A pdfm gg pdf* q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_every_pdf_03():
    r'''In scores directory.
    '''

    path = ide.PackagePath('red_score').distribution / 'red-score.pdf'
    input_ = 'pdf* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'Opening {path.trim()} ...' in transcript
