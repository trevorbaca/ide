import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_pound_01():
    r'''Addresses external file.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdi #ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('/Users/trevorbaca/abjad-ide/ide/tools/idetools/Path.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_02():
    r'''Addresses library file.
    '''

    if not abjad_ide._test_external_directory():
        return

    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path /= 'PitchArrayCell.py'

    abjad_ide('lib #PAC q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('lib #ACel q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_03():
    r'''Addresses material definition file.
    '''

    abjad_ide('red~score #agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').material('magic_numbers', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_04():
    r'''Addresses material sibling definition file backwards.
    '''

    abjad_ide('red~score %magic #< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').material('time_signatures', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_05():
    r'''Addresses material sibling definition file forwards.
    '''

    abjad_ide('red~score %magic #> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').material('performers', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_06():
    r'''Addresses segment definition file.
    '''

    abjad_ide('red~score #1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segment('segment_01', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_07():
    r'''Addresses sibling segment definition file backwards.
    '''

    abjad_ide('red~score %A #< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segment('segment_03', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_08():
    r'''Addresses sibling segment definition file forwards.
    '''

    abjad_ide('red~score %A #> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segment('segment_02', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_09():
    r'''Addresses test file.
    '''

    abjad_ide('red~score #tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test / 'test_materials.py'
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_10():
    r'''Addresses tools classfile.
    '''

    abjad_ide('red~score #RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'RhythmMaker.py'
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score #ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'ScoreTemplate.py'
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_11():
    r'''Addresses tools functionfile.
    '''

    abjad_ide('red~score #ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'adjust_spacing_sections.py'
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_pound_12():
    r'''Empty address and junk address.
    '''

    abjad_ide('# q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '#' ..." in transcript

    abjad_ide('#asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '#asdf' ..." in transcript
