import ide


def test_Menu___call___01():
    """
    Command section.
    """

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


def test_Menu___call___02():
    """
    Asset section.
    """

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

    response = menu('app,che-ban')
    assert response.payload == ['apple', 'cherry', 'banana']
    assert response.string == 'app,che-ban'

    response = menu('foo')
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.payload == ['apple']
    assert response.string == '1'


def test_Menu___call___03():
    """
    Secondary asset section.
    """

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

    response = menu('app')
    assert response.payload == ['apple']
    assert response.string == 'app'

    response = menu('app,che-ban')
    assert response.payload is None
    assert response.string == 'app,che-ban'

    response = menu('foo')
    assert response.payload is None
    assert response.string == 'foo'

    response = menu('1')
    assert response.payload is None
    assert response.string == '1'
