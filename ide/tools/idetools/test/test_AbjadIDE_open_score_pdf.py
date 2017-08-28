import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_score_pdf_01():

    target = ide.Path('red_score').distribution / 'red-score.pdf'
    input_ = 'red~score so q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert f'Opening {abjad_ide._trim(target)} ...' in transcript
    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_score_pdf_02():

    input_ = 'blue~score so q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    string = 'Missing score PDF in distribution and build directories ...'
    assert string in transcript
    assert not abjad_ide._session._attempted_to_open_file
