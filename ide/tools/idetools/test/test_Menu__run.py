# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Menu__run_01():
    r'''String menu entry defaults.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        menu_entries=commands,
        name='test', 
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'app'
    result = menu._run()
    assert result == 'apple'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    #assert result is None
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    #assert result is None
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'app, che-ban'
    result = menu._run()
    assert result is None


def test_Menu__run_02():
    r'''Hidden menu section.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        is_hidden=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'app'
    result = menu._run()
    assert result == 'apple'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'app, che-ban'
    result = menu._run()
    assert result is None


def test_Menu__run_03():
    r'''Numbered menu section.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == 'apple'

    menu._session._pending_input = 'app'
    result = menu._run()
    assert result == 'apple'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'app, che-ban'
    result = menu._run()
    assert result is None


def test_Menu__run_04():
    r'''Menu section with range selection turned on.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        is_ranged=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'app'
    result = menu._run()
    assert result == ['apple']

    menu._session._pending_input = 'app, che-ban'
    result = menu._run()
    assert result == ['apple', 'cherry', 'banana']

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None


def test_Menu__run_05():
    r'''Keyed menu section with key returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        menu_entries=commands,
        name='test',
        title='section',
        return_value_attribute='key',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == 'add'

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == 'add'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result is None


def test_Menu__run_06():
    r'''Keyed menu section with display string returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        menu_entries=commands,
        name='test',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == 'first command'

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == 'first command'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result is None


def test_Menu__run_07():
    r'''Hidden keyed menu section with key returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        is_hidden=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == 'add'

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == 'add'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result is None


def test_Menu__run_08():
    r'''Hidden keyed menu section with display string returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        is_hidden=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == 'first command'

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == 'first command'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result is None


def test_Menu__run_09():
    r'''Numbered keyed menu section with key returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == 'add'

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == 'add'

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == 'add'

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result is None


def test_Menu__run_10():
    r'''Ranged keyed menu section with with key returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        is_ranged=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == ['add']

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == ['add']

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result == ['add', 'mod', 'rm']

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result == ['add', 'mod', 'rm']

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result == ['add', 'mod', 'rm']

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None


def test_Menu__run_11():
    r'''RK menu section with display string returned.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    menu = ide.tools.idetools.Menu(
        name='test',
        session=session,
        )
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    section = menu._make_section(
        is_ranged=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    menu._session._pending_input = '<return>'
    result = menu._run()
    assert result is None

    menu._session._pending_input = 'add'
    result = menu._run()
    assert result == ['first command']

    menu._session._pending_input = 'fir'
    result = menu._run()
    assert result == ['first command']

    menu._session._pending_input = 'add, mod-rm'
    result = menu._run()
    assert result == ['first command', 'third command', 'second command']

    menu._session._pending_input = 'fir, thi-sec'
    result = menu._run()
    assert result == ['first command', 'third command', 'second command']

    menu._session._pending_input = 'fir, mod-sec'
    result = menu._run()
    assert result == ['first command', 'third command', 'second command']

    menu._session._allow_unknown_command_during_test = True
    menu._session._pending_input = 'foo'
    result = menu._run()
    assert result == 'foo'

    menu._session._pending_input = '1'
    result = menu._run()
    assert result == '1'

    menu._session._pending_input = '1, 3-2'
    result = menu._run()
    assert result is None