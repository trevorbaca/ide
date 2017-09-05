import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_definition_file_01():
    r'''In material directory.
    '''

    abjad_ide('red~score %magic df q')
    transcript = abjad_ide.io_manager.transcript 
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_02():
    r'''@-addressing to material definition file.
    '''

    abjad_ide('red~score @magic q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_03():
    r'''@-addressing to material definition file.
    '''

    abjad_ide('red~score gg @magic q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_04():
    r'''@<-addressing to sibling material definition file.
    '''

    abjad_ide('red~score %magic @< q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').materials / 'time_signatures'
    path /= 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_05():
    r'''@>-addressing to sibling material definition file.
    '''

    abjad_ide('red~score %magic @> q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').materials / 'performers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_06():
    r'''In segment directory.
    '''

    abjad_ide('red~score %A df q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_07():
    r'''@-addressing by segment name to segment definition file.
    '''

    abjad_ide('red~score @A q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_08():
    r'''@-addressing by segment number to segment definition file.
    '''

    abjad_ide('red~score @1 q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_09():
    r'''@<-addressing to sibling segment definition file.
    '''

    abjad_ide('red~score %A @< q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').segments / 'segment_03' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_10():
    r'''@>-addressing to sibling segment definition file.
    '''

    abjad_ide('red~score %A @> q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').segments / 'segment_02' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript
