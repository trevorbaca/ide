import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_check_every_definition_file_01():
    r'''In materials directory.
    '''

    abjad_ide('red~score mm dfk* q')
    transcript = abjad_ide.io.transcript
    for name in [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]:
        path = ide.Path('red_score').materials(name, 'definition.py')
        assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_every_definition_file_02():
    r'''In segments directory.
    '''

    abjad_ide('red~score gg dfk* q')
    transcript = abjad_ide.io.transcript
    for name in [
        'A',
        'B',
        'C',
        ]:
        path = ide.Path('red_score').segments(name, 'definition.py')
        assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
