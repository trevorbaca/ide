import ide


def test_Menu___call___01():
    r'''String menu entry defaults.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    menu._make_section(
        menu_entries=commands,
        name='test',
        title='section',
        )

    response = menu('app')
    assert response.known is True
    assert response.payload == 'apple'
    assert response.string == 'app'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___02():
    r'''Hidden menu section.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    menu._make_section(
        is_hidden=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    response = menu('app')
    assert response.known is True
    assert response.payload == 'apple'
    assert response.string == 'app'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___03():
    r'''Numbered menu section.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    response = menu('1')
    assert response.known is True
    assert response.payload == 'apple'
    assert response.string == '1'

    response = menu('app')
    assert response.known is True
    assert response.payload == 'apple'
    assert response.string == 'app'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'


def test_Menu___call___04():
    r'''Menu section with range selection turned on.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    menu._make_section(
        is_ranged=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    response = menu('app')
    assert response.known is True
    assert response.payload == ['apple']
    assert response.string == 'app'

    response = menu('app,che-ban')
    assert response.known is True
    assert response.payload == ['apple', 'cherry', 'banana']
    assert response.string == 'app,che-ban'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___05():
    r'''Keyed menu section with key returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        menu_entries=commands,
        name='test',
        title='section',
        return_value_attribute='key',
        )

    response = menu('add')
    assert response.known is True
    assert response.payload == 'add'
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload == 'add'
    assert response.string == 'fir'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___06():
    r'''Keyed menu section with display string returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        menu_entries=commands,
        name='test',
        )

    response = menu('add')
    assert response.known is True
    assert response.payload == 'first command'
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload == 'first command'
    assert response.string == 'fir'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___07():
    r'''Hidden keyed menu section with key returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        is_hidden=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )

    response = menu('add')
    assert response.known is True
    assert response.payload is 'add'
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload is 'add'
    assert response.string == 'fir'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___08():
    r'''Hidden keyed menu section with display string returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        is_hidden=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    response = menu('add')
    assert response.known is True
    assert response.payload == 'first command'
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload == 'first command'
    assert response.string == 'fir'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___09():
    r'''Numbered keyed menu section with key returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )

    response = menu('1')
    assert response.known is True
    assert response.payload == 'add'
    assert response.string == '1'

    response = menu('add')
    assert response.known is True
    assert response.payload == 'add'
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload == 'add'
    assert response.string == 'fir'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'


def test_Menu___call___10():
    r'''Ranged keyed menu section with with key returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        is_ranged=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )

    response = menu('add')
    assert response.known is True
    assert response.payload == ['add']
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload == ['add']
    assert response.string == 'fir'

    response = menu('add,mod-rm')
    assert response.known is True
    assert response.payload == ['add', 'mod', 'rm']
    assert response.string == 'add,mod-rm'

    response = menu('fir,thi-sec')
    assert response.known is True
    assert response.payload == ['add', 'mod', 'rm']
    assert response.string == 'fir,thi-sec'

    response = menu('fir,mod-sec')
    assert response.known is True
    assert response.payload == ['add', 'mod', 'rm']
    assert response.string == 'fir,mod-sec'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'


def test_Menu___call___11():
    r'''RK menu section with display string returned.
    '''

    io_manager = ide.IOManager(is_test=True)
    menu = ide.Menu(io_manager=io_manager, name='test')
    commands = []
    commands.append(('first command', 'add'))
    commands.append(('second command', 'rm'))
    commands.append(('third command', 'mod'))
    menu._make_section(
        is_ranged=True,
        menu_entries=commands,
        name='test',
        title='section',
        )

    response = menu('add')
    assert response.known is True
    assert response.payload == ['first command']
    assert response.string == 'add'

    response = menu('fir')
    assert response.known is True
    assert response.payload == ['first command']
    assert response.string == 'fir'

    response = menu('add,mod-rm')
    assert response.known is True
    assert response.payload == [
        'first command', 'third command', 'second command']
    assert response.string == 'add,mod-rm'

    response = menu('fir,thi-sec')
    assert response.known is True
    assert response.payload == [
        'first command', 'third command', 'second command']
    assert response.string == 'fir,thi-sec'

    response = menu('fir,mod-sec')
    assert response.known is True
    assert response.payload == [
        'first command', 'third command', 'second command']
    assert response.string == 'fir,mod-sec'

    response = menu('foo')
    assert response.known is False
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.known is False
    assert response.payload is None
    assert response.string == '1'
