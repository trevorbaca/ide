# -*- coding: utf-8 -*-
from abjad import *
import ide
session = ide.tools.idetools.Session()
io_manager = ide.tools.idetools.IOManager(session=session)


def test_Getter_append_values_01():

    getter = ide.tools.idetools.Getter()
    getter.append_integer('attribute')
    input_ = 'foo -99'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == -99


def test_Getter_append_values_02():

    getter = ide.tools.idetools.Getter()
    getter.append_integer_in_range('attribute', 1, 10)
    input_ = 'foo -99 99 7'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == 7


def test_Getter_append_values_03():

    getter = ide.tools.idetools.Getter()
    menu_entries = ['apple', 'banana', 'cherry', 'durian', 'endive', 'fennel']
    section = ide.tools.idetools.MenuSection(
        is_numbered=True,
        menu_entries=menu_entries,
        name='test',
        )
    getter.append_menu_section_range('attribute', section)
    result = [6, 5, 4, 1, 3]
    input_ = 'fen-dur, app, che'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == result


def test_Getter_append_values_04():

    getter = ide.tools.idetools.Getter()
    getter.append_string('attribute')
    input_ = 'None -99 99 1-4 foo'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) == 'foo'


def test_Getter_append_values_05():

    getter = ide.tools.idetools.Getter()
    getter.append_string_or_none('attribute')
    input_ = '-99 99 1-4 None'
    io_manager._session._pending_input = input_
    assert getter._run(io_manager=io_manager) is None