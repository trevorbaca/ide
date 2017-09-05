import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').materials / 'magic_numbers'
        path /= 'illustration.pdf'

        abjad_ide('red~score %magic pdfm pdfo q')
        transcript = abjad_ide.io_manager.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'

        abjad_ide('red~score %A pdfm pdfo q')
        transcript = abjad_ide.io_manager.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    path = ide.Path('blue_score').segments / 'segment_01'
    path /= 'illustration.pdf'

    abjad_ide('blue~score gg segment_01 pdfo q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Missing {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_04():
    r'''Allows *-addressing.
    '''

    with ide.Test():

        abjad_ide('red~score %ranges pdfm cc *ranges q')
        transcript = abjad_ide.io_manager.transcript
        path = ide.Path('red_score').materials / 'ranges' / 'illustration.pdf'
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_05():
    r'''Allows *-addressing with segment number.
    '''

    with ide.Test():
        path = ide.Path('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'

        abjad_ide('red~score %A pdfm cc *1 q')
        transcript = abjad_ide.io_manager.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_06():
    r'''*-addressing messages nonexistent file.
    '''

    path = ide.Path('red_score').materials / 'performers'
    path /= 'illustration.pdf'

    abjad_ide('red~score *performers q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Missing {path.trim()} ...' in transcript
