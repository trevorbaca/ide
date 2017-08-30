import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_segments_directory_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - segments directory',
        ]

    input_ = 'red~score mm tempi gg q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_segments_directory_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - segments directory',
        ]

    input_ = 'red~score gg A gg q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_segments_directory_03():
    r'''From score directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        ]

    input_ = 'red~score gg q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_segments_directory_04():
    r'''Makes sure reverse-order view is in effect.
    '''

    input_ = 'blue~score gg q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert '1: segment 02' in transcript
    assert '2: segment 01' in transcript
