# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
session = abjadide.idetools.Session()


def test_MenuEntry___format___01():
    r'''Formats menu section without raising exception.
    '''

    menu = abjadide.idetools.Menu(session=session)

    commands = []
    commands.append(('foo - add', 'add'))
    commands.append(('foo - delete', 'delete'))
    commands.append(('foo - modify', 'modify'))

    section = menu.make_command_section(
        commands=commands,
        name='test',
        )

    assert systemtools.TestManager.compare(
        format(section[0]),
        r'''
        idetools.MenuEntry(
            display_string='foo - add',
            key='add',
            )
        '''
        )