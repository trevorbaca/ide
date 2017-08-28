import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').materials / 'magic_numbers'
        path /= 'illustration.pdf'
        input_ = 'red~score %magic pdfm pdf q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'Opening {abjad_ide._trim(path)} ...' in transcript
        assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'
        input_ = 'red~score %A pdfm pdf q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'Opening {abjad_ide._trim(path)} ...' in transcript
        assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_03():
    r'''Displays message when PDF does not exist.
    '''

    path = ide.Path('blue_score').segments / 'segment_01' / 'illustration.pdf'
    input_ = 'blue~score gg segment~01 pdf q'
    abjad_ide._start(input_=input_)
    assert not abjad_ide._session._attempted_to_open_file
    transcript = abjad_ide._io_manager._transcript.contents
    assert f'Missing {abjad_ide._trim(path)} ...' in transcript


def test_AbjadIDE_open_pdf_04():
    r'''Allows *-addressing.
    '''

    with ide.Test():
        path = ide.Path('red_score').materials / 'ranges' / 'illustration.pdf'
        input_ = 'red~score %ranges pdfm cc *ranges q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'Opening {abjad_ide._trim(path)} ...' in transcript
        assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_05():
    r'''Allows *-addressing with segment number.
    '''

    with ide.Test():
        path = ide.Path('red_score').segments / 'segment_01'
        path /= 'illustration.pdf'
        input_ = 'red~score %A pdfm cc *1 q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'Opening {abjad_ide._trim(path)} ...' in transcript
        assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_open_pdf_06():
    r'''*-addressing messages nonexistent file.
    '''

    path = ide.Path('red_score').materials / 'performers' / 'illustration.pdf'
    input_ = 'red~score *performers q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert f'Missing {abjad_ide._trim(path)} ...' in transcript
