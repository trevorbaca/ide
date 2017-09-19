import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_caret_01():
    r'''Addresses external file.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdi ^ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('/Users/trevorbaca/abjad-ide/ide/tools/idetools/Path.py')
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_02():
    r'''Addresses library file.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('lib ^ACel q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path /= 'PitchArrayCell.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_03():
    r'''Addresses material definition file.
    '''

    abjad_ide('red~score ^agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_04():
    r'''Addresses segment definition file.
    '''

    abjad_ide('red~score ^1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_05():
    r'''Addresses test file.
    '''

    abjad_ide('red~score ^tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test / 'test_materials.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_06():
    r'''Addresses tools classfile.
    '''

    abjad_ide('red~score ^ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'ScoreTemplate.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_07():
    r'''Addresses tools functionfile.
    '''

    abjad_ide('red~score ^ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'adjust_spacing_sections.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_08():
    r'''Emtpy and junk addresses.
    '''

    abjad_ide('^ q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '^' ..." in transcript

    abjad_ide('^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '^asdf' ..." in transcript
