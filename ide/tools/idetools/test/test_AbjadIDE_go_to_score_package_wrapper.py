import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_score_package_wrapper_01():
    r'''From material directory.
    '''

    input_ = 'red~score mm tempi ww q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - package wrapper',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
    contents = abjad_ide._io_manager._transcript.contents
    assert 'red_score' in contents


def test_AbjadIDE_go_to_score_package_wrapper_02():
    r'''From segment directory.
    '''

    input_ = 'red~score gg A ww q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - package wrapper',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_score_package_wrapper_03():
    r'''From build directory.
    '''

    input_ = 'red~score bb ww q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory',
        'Red Score (2017) - package wrapper',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
