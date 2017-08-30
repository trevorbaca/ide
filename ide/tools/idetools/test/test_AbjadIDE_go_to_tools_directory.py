import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_tools_directory_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - tools directory',
        ]

    input_ = 'red~score mm tempi oo q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
    transcript = abjad_ide._transcript
    assert 'adjust_spacing_sections.py' in transcript


def test_AbjadIDE_go_to_tools_directory_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - tools directory',
        ]

    input_ = 'red~score gg A oo q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_tools_directory_03():
    r'''From score directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - tools directory',
        ]

    input_ = 'red~score oo q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_tools_directory_04():
    r'''From builds directory to tools directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - builds directory',
        'Red Score (2017) - tools directory',
        ]

    input_ = 'red~score bb oo q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
