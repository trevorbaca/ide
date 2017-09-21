import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_at_01():
    r'''Edits distribution file.
    '''

    abjad_ide('red~score @ram-not q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').distribution('red-score-program-notes.txt')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_02():
    r'''Address etc file.
    '''

    abjad_ide('red~score @notes.txt q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').etc('notes.txt')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_03():
    r'''Edits external file.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdi @ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('/Users/trevorbaca/abjad-ide/ide/tools/idetools/Path.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_04():
    r'''Edits library file.
    '''

    if not abjad_ide._test_external_directory():
        return

    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path /= 'PitchArrayCell.py'

    abjad_ide('lib @PAC q')
    transcript = abjad_ide.io.transcript 
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('lib @ACel q')
    transcript = abjad_ide.io.transcript 
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_05():
    r'''Edits material definition files.
    '''

    abjad_ide('red~score @agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').material('magic_numbers', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score mm @@fini q')
    transcript = abjad_ide.io.transcript 
    for name in [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]:
        path = ide.Path('red_score').material(name, 'definition.py')
        assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score mm @@ q')
    transcript = abjad_ide.io.transcript 
    for path in ide.Path('red_score').materials().glob('**/*'):
        if path.suffix != '.py':
            continue
        assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_06():
    r'''Edits material definition file siblings.
    '''

    abjad_ide('red~score %magic @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').material('time_signatures', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score %magic @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').material('performers', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_07():
    r'''Edits segment definition files.
    '''

    abjad_ide('red~score @1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segment('segment_01', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score gg @@efin q')
    transcript = abjad_ide.io.transcript 
    for name in [
        'segment_01',
        'segment_02',
        'segment_03',
        ]:
        path = ide.Path('red_score').segment(name, 'definition.py')
        assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score gg @@ q')
    transcript = abjad_ide.io.transcript 
    for path in ide.Path('red_score').segments().glob('**/*'):
        if path.suffix != '.py':
            continue
        assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_08():
    r'''Edits sibling segment definition files.
    '''

    abjad_ide('red~score %A @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segment('segment_03', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score %A @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segment('segment_02', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_09():
    r'''Edits stylesheet.
    '''

    abjad_ide('red~score @ext-def q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').stylesheets('context-definitions.ily')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_10():
    r'''Edits test file.
    '''

    abjad_ide('red~score @tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_11():
    r'''Edits tools files.
    '''

    abjad_ide('red~score @RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('RhythmMaker.py')
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score @ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score @ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('adjust_spacing_sections.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_12():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('@ q')
    transcript = abjad_ide.io.transcript 
    assert "No file '@' ..." in transcript

    abjad_ide('@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No file '@asdf' ..." in transcript

    abjad_ide('@@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "No file '@@asdf' ..." in transcript
