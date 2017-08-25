import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_previous_package_01():
    r'''In materials directory.
    '''

    input_ = 'red~score mm < < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - time signatures',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - materials directory - ranges',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_package_02():
    r'''In material directory.
    '''

    input_ = 'red~score mm performers < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - performers',
        'Red Score (2017) - materials directory - magic numbers',
        'Red Score (2017) - materials directory - time signatures',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_package_03():
    r'''In segments directory.
    '''

    input_ = 'red~score gg < < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - C',
        'Red Score (2017) - segments directory - B',
        'Red Score (2017) - segments directory - A',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_package_04():
    r'''In segment directory.
    '''

    input_ = 'red~score gg A < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - segments directory - C',
        'Red Score (2017) - segments directory - B',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
