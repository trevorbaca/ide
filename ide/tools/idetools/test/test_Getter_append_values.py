import ide
session = ide.Session()
io_manager = ide.IOManager(session=session)


def test_Getter_append_values_01():

    getter = ide.Getter(io_manager=io_manager)
    getter.append_string('attribute')
    input_ = '-99 99 1-4 foo'
    io_manager._session._pending_input = input_
    assert getter._run() == '-99'


def test_Getter_append_values_02():
    r'''Evaluation allows for strings of reserved words like 'map'.
    '''

    getter = ide.Getter(io_manager=io_manager)
    getter.append_string('attribute')
    input_ = 'map'
    io_manager._session._pending_input = input_
    assert getter._run() == 'map'
