import ide


def test_Session___repr___01():

    session = ide.Session(input_='foo')
    string = "Session(input_='foo')"
    assert repr(session) == string
