import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_check_every_definition_file_01():
    r'''In materials directory.
    '''

    input_ = 'red~score mm dfk* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    package_names = [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]
    paths = []
    for package_name in package_names:
        path = ide.Path('red_score')
        path = path / 'materials' / package_name / 'definition.py'
        paths.append(path)

    for path in paths:
        message = f'{abjad_ide._trim(path)} ... OK'
        assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_check_every_definition_file_02():
    r'''In segments directory.
    '''

    input_ = 'red~score gg dfk* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    package_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    paths = []
    for package_name in package_names:
        path = ide.Path('red_score')
        path = path / 'segments' / package_name / 'definition.py'
        paths.append(path)

    for path in paths:
        message = f'{abjad_ide._trim(path)} ... OK'
        assert message in contents
    assert 'Total time ' in contents
