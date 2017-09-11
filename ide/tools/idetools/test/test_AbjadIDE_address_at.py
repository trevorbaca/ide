import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_at_01():

    abjad_ide('red~score @ram-not q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').distribution / 'red-score-program-notes.txt'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_02():

    abjad_ide('red~score @notes.txt q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').etc / 'notes.txt'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_03():

    abjad_ide('red~score @agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_04():

    abjad_ide('red~score %magic @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials / 'time_signatures'
    path /= 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_05():

    abjad_ide('red~score %magic @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials / 'performers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_06():

    abjad_ide('red~score @1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_07():

    abjad_ide('red~score %A @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments / 'segment_03' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_08():

    abjad_ide('red~score %A @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments / 'segment_02' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_09():

    abjad_ide('red~score @ext-def q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').stylesheets / 'context-definitions.ily'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_10():

    abjad_ide('red~score @tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test / 'test_materials.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_11():

    abjad_ide('red~score @RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'RhythmMaker.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_12():

    abjad_ide('red~score @ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'ScoreTemplate.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_13():

    abjad_ide('red~score @ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'adjust_spacing_sections.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_14():

    abjad_ide('@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no file '@' ..." in transcript


def test_AbjadIDE_address_at_15():

    abjad_ide('@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no file '@asdf' ..." in transcript
