import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_scores_01():
    r'''Opens distribution score.
    '''

    abjad_ide('ro* q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score', 'distribution', 'red-score.pdf')
    assert f'Opening {target.trim()} ...' in transcript
