import ide


def test_AbjadIDE_edit_definition_file_01():
    r'''In material directory.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm magic~numbers df q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_edit_definition_file_02():
    r'''@-addressing to material definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score @magic q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_03():
    r'''@-addressing to material definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score gg @magic q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_04():
    r'''@<-addressing to sibling material definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm magic @< q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - magic numbers',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_05():
    r'''@>-addressing to sibling material definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm magic @> q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - magic numbers',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_06():
    r'''+-addressing to material definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score gg +magic q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - materials directory - magic numbers',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_07():
    r'''In segment directory.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score gg A df q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file


def test_AbjadIDE_edit_definition_file_08():
    r'''@-addressing by segment name to segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score @A q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_09():
    r'''@-addressing by segment name to segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm @A q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_10():
    r'''@-addressing by segment number to segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score @1 q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_11():
    r'''@<-addressing to sibling segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score gg A @< q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_12():
    r'''@>-addressing to sibling segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score gg A @> q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_13():
    r'''+-addressing by segment name to segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm +A q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - segments directory - A',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_edit_definition_file_14():
    r'''+-addressing by segment number to segment definition file.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score mm +1 q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - segments directory - A',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
