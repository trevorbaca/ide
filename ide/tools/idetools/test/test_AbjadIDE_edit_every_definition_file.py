import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_definition_file_01():
    r'''Edits every material definition.
    '''

    names = [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]
    input_ = 'red~score mm df* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert abjad_ide._session._attempted_to_open_file
    for name in names:
        path = ide.Path('red_score').materials / name / 'definition.py'
        assert f'Opening {abjad_ide._trim(path)} ...' in transcript


def test_AbjadIDE_edit_every_definition_file_02():
    r'''Edits every segment definition.
    '''

    names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    input_ = 'red~score gg df* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert abjad_ide._session._attempted_to_open_file
    for name in names:
        path = ide.Path('red_score').segments / name / 'definition.py'
        assert f'Opening {abjad_ide._trim(path)} ...' in transcript
