import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_previous_package_01():
    r'''In materials directory.
    '''

    input_ = 'red~example~score mm < < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - time signatures',
        'Red Example Score (2013) - materials directory - tempi',
        'Red Example Score (2013) - materials directory - ranges',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_package_02():
    r'''In material directory.
    '''

    input_ = 'red~example~score mm performers < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - performers',
        'Red Example Score (2013) - materials directory - magic numbers',
        'Red Example Score (2013) - materials directory - time signatures',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_package_03():
    r'''In segments directory.
    '''

    input_ = 'red~example~score gg < < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - C',
        'Red Example Score (2013) - segments directory - B',
        'Red Example Score (2013) - segments directory - A',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_package_04():
    r'''In segment directory.
    '''

    input_ = 'red~example~score gg A < < q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - segments directory - C',
        'Red Example Score (2013) - segments directory - B',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
