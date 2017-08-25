import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_segment_directory_01():
    r'''%-navigation.
    '''

    input_ = 'red~score %A q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory - A',
        ]

    assert abjad_ide._io_manager._transcript.titles == titles
    assert not abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_go_to_segment_directory_02():

    input_ = 'red~score %X q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]

    assert abjad_ide._io_manager._transcript.titles == titles
    assert "Matches no display string: '%X'." in contents


def test_AbjadIDE_go_to_segment_directory_03():
    r'''The %a should not catch tools/adjust_spacing_sections.py.
    '''

    input_ = 'red~score %a q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        ]

    assert abjad_ide._io_manager._transcript.titles == titles
    assert "Matches no display string: '%a'." in contents
