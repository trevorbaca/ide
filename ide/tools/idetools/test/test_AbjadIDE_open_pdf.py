import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():

        abjad_ide('red~score %magic pdfm q')
        path = ide.Path('red_score').materials / 'magic_numbers'
        path /= 'illustration.pdf'
        assert path.is_file()

        abjad_ide('red~score %magic pdfo q')
        transcript = abjad_ide.io.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():

        abjad_ide('red~score %A pdfm q')
        path = ide.Path('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'
        assert path.is_file()

        abjad_ide('red~score %A pdfo q')
        transcript = abjad_ide.io.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    abjad_ide('blue~score gg segment_01 pdfo q')
    path = ide.Path('blue_score').segments / 'segment_01'
    path /= 'illustration.pdf'
    transcript = abjad_ide.io.transcript
    assert f'Missing {path.trim()} ...' in transcript
