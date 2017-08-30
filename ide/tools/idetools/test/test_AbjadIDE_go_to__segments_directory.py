import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to__segments_directory_01():

    input_ = 'red~score bb _segments q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert 'Red Score (2017) - builds directory - segments' in transcript
    assert '1: segment-01.ly' in transcript
    assert '2: segment-02.ly' in transcript
    assert '3: segment-03.ly' in transcript
