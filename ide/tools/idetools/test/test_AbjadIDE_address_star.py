import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_star_01():

    abjad_ide('red~score *-score q')
    path = ide.Path('red_score').distribution / 'red-score.pdf'
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_address_star_02():

    abjad_ide('red~score %tempi pdfm q')
    path = ide.Path('red_score').materials / 'tempi' / 'illustration.pdf'
    assert path.is_file()

    abjad_ide('red~score *tempi q')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_address_star_03():

    abjad_ide('red~score %A pdfm q')
    path = ide.Path('red_score').segments / 'segment_01' / 'illustration.pdf'
    assert path.is_file()

    abjad_ide('red~score *A q')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript

    abjad_ide('red~score *1 q')
    transcript = abjad_ide.io.transcript 
    assert f'Opening {path.trim()} ...' in transcript


def test_AbjadIDE_address_star_04():

    abjad_ide('* q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no PDF '*' ..." in transcript


def test_AbjadIDE_address_star_05():

    abjad_ide('*asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no PDF '*asdf' ..." in transcript
