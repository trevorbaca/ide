import ide


def test_Getter_predicates_01():

    assert ide.Getter.is_boolean(True)
    assert ide.Getter.is_boolean(False)

    assert not ide.Getter.is_boolean(None)
    assert not ide.Getter.is_boolean('')
    assert not ide.Getter.is_boolean(0)
    assert not ide.Getter.is_boolean(1)


def test_Getter_predicates_02():

    assert not ide.Getter.is_boolean(None)
    assert not ide.Getter.is_boolean('')
    assert not ide.Getter.is_boolean('1')
    assert not ide.Getter.is_boolean('foo_!')
    assert not ide.Getter.is_boolean('foo_#')
    assert not ide.Getter.is_boolean('foo_@')
