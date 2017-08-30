import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE__handle_input_01():
    r'''Handles numeric input.
    '''

    input_ = 'red~score dd 1 q'
    abjad_ide._start(input_=input_)


def test_AbjadIDE__handle_input_02():
    r'''Handles empty addressing.
    '''

    input_ = '@ % ^ * + q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert "Matches no display string '@' ..." in transcript
    assert "Matches no display string '%' ..." in transcript
    assert "Matches no display string '^' ..." in transcript
    assert "Matches no display string '*' ..." in transcript
    assert "Matches no display string '+' ..." in transcript


def test_AbjadIDE__handle_input_03():
    r'''Handles missing addresses.
    '''

    input_ = '%letter'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert "Matches no display string '%letter' ..." in transcript
