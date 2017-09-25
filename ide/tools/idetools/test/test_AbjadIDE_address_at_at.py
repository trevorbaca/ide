import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_at_at_01():
    r'''Edits material definition files.
    '''

    abjad_ide('red mm @@fini q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@fini' to 5 files ..." in transcript
    for name in [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]:
        path = ide.Path('red_score').materials(name, 'definition.py')
        assert f'{path.trim()} ...' in transcript

    abjad_ide('red mm @@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@' to 8 files ..." in transcript


def test_AbjadIDE_address_at_at_02():
    r'''Edits segment definition files.
    '''

    abjad_ide('red gg @@efin q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@efin' to 3 files ..." in transcript
    for name in [
        'A',
        'B',
        'C',
        ]:
        path = ide.Path('red_score').segments(name, 'definition.py')
        assert f'{path.trim()} ...' in transcript

    abjad_ide('red gg @@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@' to 6 files ..." in transcript


def test_AbjadIDE_address_at_at_03():
    r'''Handles double-prefix numeric input.
    '''

    abjad_ide('red mm @@0 q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@@0' to no files ..." in transcript

    abjad_ide('red mm @@1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'materials', 'magic_numbers', 'definition.py')
    assert f"Matching '@@1' to {path.trim()} ..." in transcript

    abjad_ide('red mm @@99 q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@@99' to no files ..." in transcript


def test_AbjadIDE_address_at_at_04():
    r'''Handles empty input, junk input and nonfile input.
    '''

    abjad_ide('@@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@asdf' to no files ..." in transcript


def test_AbjadIDE_address_at_at_05():
    r'''Provides warning with <= 20 files.
    '''

    abjad_ide('red @@ <return> q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@@' to 35 files ..."
    assert '35 files ok?> ' in transcript
