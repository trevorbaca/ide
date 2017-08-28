import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_check_every_definition_file_01():
    r'''In materials directory.
    '''

    package_names = [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]
    input_ = 'red~score mm dfk* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    for package_name in package_names:
        path = ide.Path('red_score').materials / package_name / 'definition.py'
        assert f'{abjad_ide._trim(path)} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_every_definition_file_02():
    r'''In segments directory.
    '''

    package_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    input_ = 'red~score gg dfk* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    for package_name in package_names:
        path = ide.Path('red_score').segments / package_name / 'definition.py'
        assert f'{abjad_ide._trim(path)} ... OK' in transcript
    assert 'Total time ' in transcript
