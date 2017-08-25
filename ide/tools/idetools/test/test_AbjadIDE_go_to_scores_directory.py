import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_scores_directory_01():
    r'''From material directory.
    '''

    input_ = 'red~score mm tempi ss q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Abjad IDE - scores directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_scores_directory_02():
    r'''From segment directory.
    '''

    input_ = 'red~score gg A ss q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Abjad IDE - scores directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_scores_directory_03():
    r'''From score directory.
    '''

    input_ = 'red~score ss q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Abjad IDE - scores directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_scores_directory_04():
    r'''From home to home.
    '''

    input_ = 'ss q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Abjad IDE - scores directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
