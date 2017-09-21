import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_caret_01():
    r'''Addresses external file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi ^ath q')
    transcript = abjad_ide.io.transcript 
    assert f'Running doctest on Path.py ...' in transcript


def test_AbjadIDE_address_caret_02():
    r'''Addresses library file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll ^ACel q')
    transcript = abjad_ide.io.transcript 
    assert f'Running doctest on PitchArrayCell.py ...' in transcript


def test_AbjadIDE_address_caret_03():
    r'''Addresses material definition files.
    '''

    abjad_ide('red~score ^agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').material('magic_numbers', 'definition.py')
    assert f'Running doctest on {path.trim()} ...' in transcript

    abjad_ide('red~score mm ^^efin q')
    transcript = abjad_ide.io.transcript 
    assert f'Running doctest on 5 modules ...' in transcript

    abjad_ide('red~score mm ^^ q')
    transcript = abjad_ide.io.transcript 
    assert f'Running doctest on 25 modules ...' in transcript


def test_AbjadIDE_address_caret_04():
    r'''Addresses segment definition files.
    '''

    abjad_ide('red~score ^1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segment('segment_01', 'definition.py')
    assert f'Running doctest on {path.trim()} ...' in transcript

    abjad_ide('red~score gg ^^efin q')
    transcript = abjad_ide.io.transcript 
    assert f'Running doctest on 3 modules ...' in transcript

    abjad_ide('red~score gg ^^ q')
    transcript = abjad_ide.io.transcript 
    assert f'Running doctest on 18 modules ...' in transcript


def test_AbjadIDE_address_caret_05():
    r'''Addresses test file.
    '''

    abjad_ide('red~score ^tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_06():
    r'''Addresses tools files.
    '''

    abjad_ide('red~score ^ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f'Running doctest on {path.trim()} ...' in transcript

    abjad_ide('red~score ^ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('adjust_spacing_sections.py')
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_07():
    r'''Emtpy and junk addresses.
    '''

    abjad_ide('^ q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '^' ..." in transcript

    abjad_ide('^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '^asdf' ..." in transcript

    abjad_ide('^^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '^^asdf' ..." in transcript
