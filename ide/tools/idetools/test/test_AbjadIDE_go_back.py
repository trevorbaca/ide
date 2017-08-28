import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_back_01():

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - tools directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - tools directory',
        ]

    input_ = 'red~score mm tempi oo - - q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_back_02():

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - build directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - build directory',
        ]

    input_ = 'red~score gg A bb - - q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_back_03():

    titles = [
        'Abjad IDE - scores directory',
        ]

    input_ = '- q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_back_04():

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Abjad IDE - scores directory',
        ]

    input_ = 'red~score - - - q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
