import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_star_01():
    r'''Opens distribution PDF.
    '''

    abjad_ide('red~score *-score q')
    path = ide.Path('red_score').distribution('red-score.pdf')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_address_star_02():
    r'''Opens material PDF.
    '''

    abjad_ide('red~score %tempi pdfm q')
    path = ide.Path('red_score').material('tempi', 'illustration.pdf')
    assert path.is_file()

    abjad_ide('red~score *tempi q')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_address_star_03():
    r'''Opens segment PDF.
    '''

    abjad_ide('red~score %A pdfm q')
    path = ide.Path('red_score').segment('segment_01', 'illustration.pdf')
    assert path.is_file()

    abjad_ide('red~score *A q')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript

    abjad_ide('red~score *1 q')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_address_star_04():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('* q')
    transcript = abjad_ide.io.transcript 
    assert "No PDF '*' ..." in transcript

    abjad_ide('*asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No PDF '*asdf' ..." in transcript
