import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_tools_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red~score mm tempi oo q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : tools',
        ]
    assert 'adjust_spacing_sections.py' in transcript


def test_AbjadIDE_go_to_tools_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red~score gg A oo q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : tools',
        ]


def test_AbjadIDE_go_to_tools_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red~score oo q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : tools',
        ]


def test_AbjadIDE_go_to_tools_directory_04():
    r'''From builds directory to tools directory.
    '''


    abjad_ide('red~score bb oo q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : tools',
        ]
