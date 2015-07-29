# -*- encoding: utf -*-
import codecs
import os
import sys
from abjad.tools import stringtools


class Controller(object):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_io_manager',
        '_session',
        '_transcript',
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        from ide.tools import idetools
        self._configuration = idetools.Configuration()
        self._session = session or idetools.Session()
        self._io_manager = idetools.IOManager(
            client=self,
            session=self._session,
            )
        self._transcript = self._session.transcript

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    def __hash__(self):
        r'''Hashes controller.
        '''
        return hash((type(self), self._session))

    def __ne__(self, expr):
        r'''Is true when types are not the same. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Gets interpreter representation of controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    @property
    def _breadcrumb(self):
        pass

    @property
    def _command_to_method(self):
        result = {
            'b': self.go_back,
            'q': self.quit,
            's': self.go_to_current_score,
            'h': self.go_to_all_scores,
            }
        return result

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(type(self).__name__)

    @property
    def _tab(self):
        return 4 * ' '

    ### PRIVATE METHODS ###

    @staticmethod
    def _remove_file_line(file_path, line_to_remove):
        lines_to_keep = []
        with open(file_path, 'r') as file_pointer:
            for line in file_pointer.readlines():
                if line == line_to_remove:
                    pass
                else:
                    lines_to_keep.append(line)
        with open(file_path, 'w') as file_pointer:
            contents = ''.join(lines_to_keep)
            file_pointer.write(contents)

    @staticmethod
    def _replace_in_file(file_path, old, new):
        assert isinstance(old, str), repr(old)
        assert isinstance(new, str), repr(new)
        with open(file_path, 'r') as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        new_file_contents = ''.join(new_file_lines)
        if sys.version_info[0] == 2:
            new_file_contents = unicode(new_file_contents, 'utf-8')
            with codecs.open(file_path, 'w', encoding='utf-8') as file_pointer:
                file_pointer.write(new_file_contents)
        else:
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(new_file_contents)

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary
        
    @staticmethod
    def _trim_path(path, width=80):
        if width and width < len(path):
            path = '...' + path[-width:]
        return path

    ### PUBLIC METHODS ###

    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._display_available_commands = False

    def go_to_all_scores(self):
        r'''Goes to all scores.

        Returns none.
        '''
        self._session._is_navigating_home = False
        self._session._is_navigating_to_scores = True
        self._session._display_available_commands = False

    def go_to_current_score(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._display_available_commands = False

    def quit(self):
        r'''Quits.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_available_commands = False