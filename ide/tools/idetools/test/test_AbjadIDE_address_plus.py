import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_plus_01():
    r'''Tests external file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi +ath q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on Path.py ...' in transcript


def test_AbjadIDE_address_plus_02():
    r'''Tests library file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll +PAC q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on 2 modules ...' in transcript

    abjad_ide('ll +ACel q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on PitchArrayCell.py ...' in transcript


def test_AbjadIDE_address_plus_03():
    r'''Tests material definition files.
    '''

    abjad_ide('red~score +agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').material('magic_numbers', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score mm ++defini q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on 5 modules ...' in transcript

    abjad_ide('red~score mm ++ q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on 25 modules ...' in transcript


def test_AbjadIDE_address_plus_04():
    r'''Tests material sibling definition files.
    '''

    abjad_ide('red~score %magic +< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').material('time_signatures', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score %magic +> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').material('performers', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_plus_05():
    r'''Tests segment definition file.
    '''

    abjad_ide('red~score +1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segment('segment_01', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score gg ++defi q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on 3 modules ...' in transcript

    abjad_ide('red~score gg ++ q')
    transcript = abjad_ide.io.transcript 
    assert f'Running pytest on 18 modules ...' in transcript


def test_AbjadIDE_address_plus_06():
    r'''Tests sibling segment definition files.
    '''

    abjad_ide('red~score %A +< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segment('segment_03', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score %A +> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segment('segment_02', 'definition.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_plus_07():
    r'''Tests test file.
    '''

    abjad_ide('red~score +tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_plus_08():
    r'''Tests tools files.
    '''

    abjad_ide('red~score +RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('RhythmMaker.py')
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score +ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f'Running pytest on {path.trim()} ...' in transcript

    abjad_ide('red~score +ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('adjust_spacing_sections.py')
    assert f'Running pytest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_plus_09():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('+ q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '+' ..." in transcript

    abjad_ide('+asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '+asdf' ..." in transcript

    abjad_ide('++asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No Python file '++asdf' ..." in transcript
