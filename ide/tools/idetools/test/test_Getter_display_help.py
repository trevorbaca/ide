import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_Getter_display_help_01():
    r'''Question mark displays help.
    '''

    input_ = 'red~score mm new ? <return> q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript

    string = 'Value must be string.'
    assert string in transcript


def test_Getter_display_help_02():
    r'''Help string displays help.
    '''

    input_ = 'red~score mm new help <return> q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript

    string = 'Value must be string.'
    assert string in transcript
