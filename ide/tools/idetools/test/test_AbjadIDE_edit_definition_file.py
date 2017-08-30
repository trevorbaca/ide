import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_definition_file_01():
    r'''In material directory.
    '''

    path = ide.PackagePath('red_score').materials / 'magic_numbers'
    path /= 'definition.py'

    input_ = 'red~score %magic~numbers df q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_02():
    r'''@-addressing to material definition file.
    '''

    path = ide.PackagePath('red_score').materials / 'magic_numbers'
    path /= 'definition.py'

    input_ = 'red~score @magic q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_03():
    r'''@-addressing to material definition file.
    '''

    path = ide.PackagePath('red_score').materials / 'magic_numbers'
    path /= 'definition.py'

    input_ = 'red~score gg @magic q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_04():
    r'''@<-addressing to sibling material definition file.
    '''

    path = ide.PackagePath('red_score').materials / 'time_signatures'
    path /= 'definition.py'

    input_ = 'red~score %magic @< q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_05():
    r'''@>-addressing to sibling material definition file.
    '''

    path = ide.PackagePath('red_score').materials / 'performers'
    path /= 'definition.py'

    input_ = 'red~score %magic @> q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_06():
    r'''+-addressing to material definition file.
    '''

    path = ide.PackagePath('red_score').materials / 'magic_numbers'
    path /= 'definition.py'

    input_ = 'red~score gg +magic q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_07():
    r'''In segment directory.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_01'
    path /= 'definition.py'

    input_ = 'red~score %A df q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_08():
    r'''@-addressing by segment name to segment definition file.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_01'
    path /= 'definition.py'

    input_ = 'red~score @A q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_09():
    r'''@-addressing by segment number to segment definition file.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_01'
    path /= 'definition.py'

    input_ = 'red~score @1 q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_10():
    r'''@<-addressing to sibling segment definition file.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_03'
    path /= 'definition.py'

    input_ = 'red~score %A @< q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_11():
    r'''@>-addressing to sibling segment definition file.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_02'
    path /= 'definition.py'

    input_ = 'red~score %A @> q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_12():
    r'''+-addressing by segment name to segment definition file.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_01'
    path /= 'definition.py'

    input_ = 'red~score +A q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_definition_file_13():
    r'''+-addressing by segment number to segment definition file.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_01'
    path /= 'definition.py'

    input_ = 'red~score mm +1 q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript
