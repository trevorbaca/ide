import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_score_pdf_01():
    r'''Opens distribution score.
    '''

    abjad_ide('red rpo q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score', 'distribution', 'red-score.pdf')
    assert f'Opening {target.trim()} ...' in transcript


def test_AbjadIDE_open_score_pdf_02():
    r'''Opens build score.
    '''

    abjad_ide('red %letter rpo q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score', 'builds', 'letter-score', 'score.pdf')
    assert f'No files ending in *score.pdf ...' in transcript


def test_AbjadIDE_open_score_pdf_03():

    abjad_ide('blu rpo q')
    transcript = abjad_ide.io.transcript
    string = 'Missing score PDF in distribution and build directories ...'
    assert string in transcript
