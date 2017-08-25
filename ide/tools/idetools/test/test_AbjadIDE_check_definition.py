import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_check_definition_01():
    r'''In material directory.
    '''

    path = ide.Path('red_score')
    path = path / 'materials' / 'magic_numbers' / 'definition.py'

    input_ = 'red~score %magic dfk q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    message = f'{abjad_ide._trim(path)} ... OK'
    assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_check_definition_02():
    r'''In segment directory.
    '''

    path = ide.Path('red_score')
    path = path / 'segments' / 'segment_01' / 'definition.py'

    input_ = 'red~score %A dfk q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    message = f'{abjad_ide._trim(path)} ... OK'
    assert message in contents
    assert 'Total time ' in contents
