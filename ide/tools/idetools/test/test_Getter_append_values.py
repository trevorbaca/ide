import ide
session = ide.Session()
io_manager = ide.IOManager(session=session)


def test_Getter_append_values_01():

    getter = ide.Getter()
    getter.append_integer('attribute')
    input_ = 'foo -99'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == -99


def test_Getter_append_values_02():

    getter = ide.Getter()
    getter.append_integer_in_range('attribute', 1, 10)
    input_ = 'foo -99 99 7'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == 7


def test_Getter_append_values_03():

    getter = ide.Getter()
    getter.append_string('attribute')
    input_ = '-99 99 1-4 foo'
    io_manager._session._pending_input = input_
    #assert getter._run(io_manager=io_manager) == 'foo'
    assert getter._run(io_manager=io_manager) == '-99'


def test_Getter_append_values_04():
    r'''Evaluation allows for strings of reserved words like 'map'.
    '''

    getter = ide.Getter()
    getter.append_string('attribute')
    input_ = 'map'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == 'map'
