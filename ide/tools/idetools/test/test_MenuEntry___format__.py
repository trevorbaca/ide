# -*- coding: utf-8 -*-
import abjad
import ide


def test_MenuEntry___format___01():
    r'''Formats menu section without raising exception.
    '''

    menu = ide.tools.idetools.Menu()

    commands = []
    commands.append(('foo - add', 'add'))
    commands.append(('foo - delete', 'delete'))
    commands.append(('foo - modify', 'modify'))

    section = menu.make_command_section(
        commands=commands,
        name='test',
        )

    assert abjad.systemtools.TestManager.compare(
        format(section[0]),
        r'''
        idetools.MenuEntry(
            display_string='foo - add',
            key='add',
            )
        '''
        )