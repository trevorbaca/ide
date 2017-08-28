import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_build_directory_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - build directory',
        ]

    input_ = 'red~score mm tempi bb q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_build_directory_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - build directory',
        ]

    input_ = 'red~score gg A bb q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_build_directory_03():
    r'''From score directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - distribution directory',
        ]

    input_ = 'red~score dd q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_build_directory_04():
    r'''From build directory to build directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory',
        'Red Score (2017) - build directory',
        ]

    input_ = 'red~score bb bb q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_build_directory_05():
    r'''Git ignore file is hidden.
    '''

    input_ = 'red~score bb q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert '.gitignore' not in transcript
