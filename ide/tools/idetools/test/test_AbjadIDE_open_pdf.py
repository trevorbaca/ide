import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():

        abjad_ide('red %rpc pdfm q')
        path = ide.Path(
            'red_score', 'materials', 'red_pitch_classes', 'illustration.pdf')
        assert path.is_file()

        abjad_ide('red %rpc pdfo q')
        transcript = abjad_ide.io.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():

        abjad_ide('red %A pdfm q')
        path = ide.Path('red_score', 'segments', 'A', 'illustration.pdf')
        assert path.is_file()

        abjad_ide('red %A pdfo q')
        transcript = abjad_ide.io.transcript
        assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    abjad_ide('blu %A pdfo q')
    path = ide.Path('blue_score', 'segments', 'A', 'illustration.pdf')
    transcript = abjad_ide.io.transcript
    assert f'Missing {path.trim()} ...' in transcript
