import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_score_pdf_01():

    target = ide.PackagePath('red_score').distribution / 'red-score.pdf'
    input_ = 'red~score spdfo q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'Opening {target.trim()} ...' in transcript


def test_AbjadIDE_open_score_pdf_02():

    input_ = 'blue~score spdfo q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    string = 'Missing score PDF in distribution and build directories ...'
    assert string in transcript
