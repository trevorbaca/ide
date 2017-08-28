import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_Menu__change_input_to_directive_01():
    r'''Works with mixed case.
    '''

    input_ = 'Red~score q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    string = 'Red Score (2017)'
    assert string in transcript


def test_Menu__change_input_to_directive_02():
    r'''Works with mixed case.
    '''

    input_ = 'red~Score q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    string = 'Red Score (2017)'
    assert string in transcript


def test_Menu__change_input_to_directive_03():
    r'''Works with mixed case.
    '''

    input_ = 'red~example~Score q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    string = 'Red Score (2017)'
    assert string in transcript


def test_Menu__change_input_to_directive_04():
    r'''Works with mixed case.
    '''

    input_ = 'RED~SCORE q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    string = 'Red Score (2017)'
    assert string in transcript


def test_Menu__change_input_to_directive_05():
    r'''Material that is list of numbers does not alias numeric assets entry.

    The '1' in the input below is correctly interpret as the __init__.py file,
    assigned the number 1. in the menu section; this is not aliased by the
    presence of the number 1 in the series of magic numbers itself:
    1, 3, 4, 7, ....
    '''

    input_ = 'red~score mm magic~numbers 1 q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file
