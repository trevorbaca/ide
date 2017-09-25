import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_star_01():
    r'''In contents directory.
    '''

    abjad_ide('red *-score q')
    path = ide.Path('red_score', 'distribution', 'red-score.pdf')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '*-score' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_star_02():
    r'''In material directory.
    '''

    with ide.Test():

        abjad_ide('red %tempi pdfm q')
        path = ide.Path('red_score', 'materials', 'tempi', 'illustration.pdf')
        assert path.is_file()

        abjad_ide('red *tempi q')
        transcript = abjad_ide.io.transcript 
        assert f"Matching '*tempi' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_star_03():
    r'''In segment directory.
    '''

    with ide.Test():

        abjad_ide('red %A pdfm q')
        path = ide.Path('red_score', 'segments', 'A', 'illustration.pdf')
        assert path.is_file()

        abjad_ide('red *A q')
        transcript = abjad_ide.io.transcript 
        assert f"Matching '*A' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_star_04():
    r'''Handles single-prefix numeric input.
    '''

    with ide.Test():
        path = ide.Path('red_score', 'segments', 'A', 'illustration.pdf')

        abjad_ide('red %A pdfm q')
        assert path.is_file()

        abjad_ide('red gg *0 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '*0' to no PDFs ..." in transcript

        abjad_ide('red gg *1 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '*1' to {path.trim()} ..." in transcript

        abjad_ide('red gg *99 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '*99' to no PDFs ..." in transcript


def test_AbjadIDE_address_star_05():
    r'''Handles double-prefix numeric input.
    '''

    with ide.Test():
        path = ide.Path('red_score', 'segments', 'A', 'illustration.pdf')

        abjad_ide('red %A pdfm q')
        assert path.is_file()

        abjad_ide('red gg **0 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '**0' to no PDFs ..." in transcript

        abjad_ide('red gg **1 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '**1' to {path.trim()} ..." in transcript

        abjad_ide('red gg **99 q')
        transcript = abjad_ide.io.transcript
        assert f"Matching '**99' to no PDFs ..." in transcript


def test_AbjadIDE_address_star_06():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('* q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '*' to no PDFs ..." in transcript

    abjad_ide('*asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '*asdf' to no PDFs ..." in transcript
