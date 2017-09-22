import ide


def test_Menu___call___01():
    r'''Asset section.
    '''

    menu = ide.Menu(
        sections=[
            ide.MenuSection(
                entries=[
                    ('apple', 'apple'),
                    ('banana', 'banana'),
                    ('cherry', 'cherry'),
                    ],
                ),
            ],
        )

    response = menu('app')
    assert response.payload == ['apple']
    assert response.string == 'app'

    response = menu('foo')
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.payload == 'apple'
    assert response.string == '1'


def test_Menu___call___02():
    r'''Secondary asset section.
    '''

    menu = ide.Menu(
        sections=[
            ide.MenuSection(
                entries=[
                    ('apple', 'apple'),
                    ('banana', 'banana'),
                    ('cherry', 'cherry'),
                    ],
                secondary=True,
                ),
            ],
        )

    response = menu('1')
    assert response.payload is None
    assert response.string == '1'

    response = menu('app')
    assert response.payload == ['apple']
    assert response.string == 'app'

    response = menu('foo')
    assert response.payload is None
    assert response.string == 'foo'


def test_Menu___call___03():
    r'''Asset section with multiple selection turned on.
    '''

    menu = ide.Menu(
        sections=[
            ide.MenuSection(
                entries=[
                    ('apple', 'apple'),
                    ('banana', 'banana'),
                    ('cherry', 'cherry'),
                    ],
                multiple=True,
                ),
            ],
        )

    response = menu('app')
    assert response.payload == ['apple']
    assert response.string == 'app'

    response = menu('app,che-ban')
    assert response.payload == ['apple', 'cherry', 'banana']
    assert response.string == 'app,che-ban'

    response = menu('foo')
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.payload == ['apple']
    assert response.string == '1'


def test_Menu___call___04():
    r'''Command section.
    '''

    menu = ide.Menu(
        sections=[
            ide.MenuSection(
                entries=[
                    ('first command', 'add'),
                    ('second command', 'rm'),
                    ('third command', 'mod'),
                    ],
                command='path',
                ),
            ],
        )

    response = menu('add')
    assert response.payload == 'add'
    assert response.string == 'add'

    response = menu('fir')
    assert response.payload is None
    assert response.string == 'fir'

    response = menu('foo')
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.payload is None
    assert response.string == '1'
