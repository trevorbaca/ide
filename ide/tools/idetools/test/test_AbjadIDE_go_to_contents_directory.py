import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_contents_directory_01():
    r'''From material directory.
    '''

    input_ = 'red~score mm tempi cc q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_contents_directory_02():
    r'''From segment directory.
    '''

    input_ = 'red~score gg A cc q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_contents_directory_03():
    r'''From score directory.
    '''

    input_ = 'red~score cc q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_contents_directory_04():
    r'''From build directory.
    '''

    input_ = 'red~score bb cc q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory',
        'Red Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_contents_directory_05():
    r'''With substring matching.
    '''

    input_ = 'lue q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Blue Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_contents_directory_06():
    r'''With capital letter matching.
    '''

    input_ = 'BS q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Blue Score (2017)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
