import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_score_pdf_01():
    r'''Opens distribution score.
    '''

    abjad_ide('red~score so q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score').distribution('red-score.pdf')
    assert f'Opening {target.trim()} ...' in transcript


def test_AbjadIDE_open_score_pdf_02():
    r'''Opens build score.
    '''

    abjad_ide('red~score %letter so q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score').build('letter', 'score.pdf')
    assert f'Missing {target.trim()} ...' in transcript


def test_AbjadIDE_open_score_pdf_03():

    abjad_ide('blue~score so q')
    transcript = abjad_ide.io.transcript
    string = 'Missing score PDF in distribution and build directories ...'
    assert string in transcript
