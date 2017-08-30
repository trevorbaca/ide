import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_wrapper_directory_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - wrapper directory',
        ]

    input_ = 'red~score mm tempi ww q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
    transcrtip = abjad_ide._transcript
    assert 'red_score' in transcrtip


def test_AbjadIDE_go_to_wrapper_directory_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - wrapper directory',
        ]

    input_ = 'red~score gg A ww q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_wrapper_directory_03():
    r'''From builds directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - builds directory',
        'Red Score (2017) - wrapper directory',
        ]

    input_ = 'red~score bb ww q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
