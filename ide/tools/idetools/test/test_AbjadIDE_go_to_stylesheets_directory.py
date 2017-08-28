import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_stylesheets_directory_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - stylesheets directory',
        ]

    input_ = 'red~score mm tempi yy q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_stylesheets_directory_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - stylesheets directory',
        ]

    input_ = 'red~score gg A yy q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_stylesheets_directory_03():
    r'''From score directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - stylesheets directory',
        ]

    input_ = 'red~score yy q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_stylesheets_directory_04():
    r'''Goes from build directory to stylesheets directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory',
        'Red Score (2017) - stylesheets directory',
        ]

    input_ = 'red~score bb yy q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
