import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_smart_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():

        abjad_ide('red %metronome pdfm q')
        path = ide.Path(
            'red_score', 'materials', 'metronome_marks', 'illustration.pdf')
        assert path.is_file()

        abjad_ide('red *metronome q')
        transcript = abjad_ide.io.transcript 
        assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_smart_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        path = ide.Path('red_score', 'segments', 'A', 'illustration.pdf')

        abjad_ide('red %A pdfm q')
        assert path.is_file()

        abjad_ide('red *A q')
        transcript = abjad_ide.io.transcript 
        assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_smart_pdf_03():
    r'''Handles numbers.
    '''

    with ide.Test():
        path = ide.Path('red_score', 'segments', '_', 'illustration.pdf')

        abjad_ide('red %_ pdfm q')
        assert path.is_file()

        abjad_ide('red gg *0 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '*0' to 0 files ..." in transcript

        abjad_ide('red gg *1 q')
        transcript = abjad_ide.io.transcript
        assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_smart_pdf_04():
    r'''Missing pattern.
    '''

    abjad_ide('* q')
    transcript = abjad_ide.io.transcript 
    assert "Missing '*' pattern ..." in transcript


def test_AbjadIDE_smart_pdf_05():
    r'''Unmatched pattern.
    '''

    abjad_ide('*asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '*asdf' to 0 files ..." in transcript
