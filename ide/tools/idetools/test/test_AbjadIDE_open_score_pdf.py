import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_score_pdf_01():

    abjad_ide('red~score spdfo q')
    transcript = abjad_ide.io_manager.transcript
    target = ide.Path('red_score').distribution / 'red-score.pdf'
    assert f'Opening {target.trim()} ...' in transcript


def test_AbjadIDE_open_score_pdf_02():

    abjad_ide('blue~score spdfo q')
    transcript = abjad_ide.io_manager.transcript
    string = 'Missing score PDF in distribution and build directories ...'
    assert string in transcript
