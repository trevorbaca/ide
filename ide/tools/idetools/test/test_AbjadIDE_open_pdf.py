import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        path = ide.PackagePath('red_score').materials / 'magic_numbers'
        path /= 'illustration.pdf'

        input_ = 'red~score %magic pdfm pdfo q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        path = ide.PackagePath('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'

        input_ = 'red~score %A pdfm pdfo q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    path = ide.PackagePath('blue_score').segments / 'segment_01'
    path /= 'illustration.pdf'

    input_ = 'blue~score gg segment~01 pdfo q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'Missing {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_04():
    r'''Allows *-addressing.
    '''

    with ide.Test():
        path = ide.PackagePath('red_score').materials / 'ranges' / 'illustration.pdf'
        input_ = 'red~score %ranges pdfm cc *ranges q'

        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_05():
    r'''Allows *-addressing with segment number.
    '''

    with ide.Test():
        path = ide.PackagePath('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'

        input_ = 'red~score %A pdfm cc *1 q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_06():
    r'''*-addressing messages nonexistent file.
    '''

    path = ide.PackagePath('red_score').materials / 'performers'
    path /= 'illustration.pdf'

    input_ = 'red~score *performers q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'Missing {path.trim()} ...' in transcript
