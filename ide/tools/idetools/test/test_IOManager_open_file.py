import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_IOManager_open_file_01():
    r'''@-addressing to distribution file.
    '''

    input_ = 'red~score @program-notes.txt q'
    abjad_ide._start(input_=input_)


    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_02():
    r'''@-addressing to etc file.
    '''

    input_ = 'red~score @notes.txt q'
    abjad_ide._start(input_=input_)


    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_03():
    r'''@-addressing to tools file.
    '''

    input_ = 'red~score @RM q'
    abjad_ide._start(input_=input_)


    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_04():
    r'''@-addressing to tools file with line number
    '''

    input_ = 'red~score @RM+14 q'
    abjad_ide._start(input_=input_)


    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_IOManager_open_file_05():
    r'''@-addressing to stylesheet.
    '''

    input_ = 'red~score @gasso q'
    abjad_ide._start(input_=input_)


    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
