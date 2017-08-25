import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    input_ = 'red~score %magic pdfm pdf q'
    with ide.Test():
        abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    input_ = 'red~score %A pdfm pdf q'
    with ide.Test():
        abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    input_ = 'blue~score gg segment~01 pdf q'
    abjad_ide._start(input_=input_)
    assert not abjad_ide._session._attempted_to_open_file
    contents = abjad_ide._io_manager._transcript.contents
    assert 'File does not exist:' in contents


def test_AbjadIDE_open_pdf_04():
    r'''Allows *-addressing.
    '''

    input_ = 'red~score %ranges pdfm cc *ranges q'
    with ide.Test():
        abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_05():
    r'''Allows *-addressing with segment number.
    '''

    input_ = 'red~score %A pdfm cc *1 q'
    with ide.Test():
        abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_06():
    r'''*-addressing messages nonexistent file.
    '''

    input_ = 'red~score *performer q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'File does not exist:' in contents
