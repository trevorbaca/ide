# -*- encoding: utf-8 -*-


class Session(object):
    r'''Abjad IDE session.

        ::

            >>> session = ide.tools.idetools.Session()
            >>> session
            Session()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_unknown_command_during_test',
        '_after_redraw_message',
        '_attempted_method',
        '_attempted_to_open_file',
        '_clear_terminal_after_quit',
        '_confirm',
        '_display',
        '_is_in_confirmation_environment',
        '_is_quitting',
        '_is_test',
        '_last_asset_path',
        '_last_score_path',
        '_manifest_current_directory',
        '_pending_input',
        '_pending_redraw',
        )

    ### INITIALIZER ###

    def __init__(self, input_=None, is_test=False):
        from ide.tools import idetools
        self._after_redraw_message = None
        self._allow_unknown_command_during_test = False
        self._attempted_method = None
        self._attempted_to_open_file = False
        self._clear_terminal_after_quit = False
        self._confirm = True
        self._display = True
        self._is_in_confirmation_environment = False
        self._is_quitting = False
        self._is_test = is_test
        self._last_asset_path = None
        self._last_score_path = None
        self._manifest_current_directory = None
        self._pending_input = input_
        self._pending_redraw = True

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of session.

        ..  container:: example

            ::

                >>> session
                Session()

        Returns string.
        '''
        summary = []
        if self.pending_input not in (None, ''):
            string = 'input_={!r}'
            string = string.format(self.pending_input)
            summary.append(string)
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    ### PRIVATE METHODS ###

    def _reinitialize(self):
        is_test = self._is_test
        allow_unknown = self._allow_unknown_command_during_test
        type(self).__init__(self, is_test=self.is_test)
        self._allow_unknown_command_during_test = allow_unknown

    ### PUBLIC PROPERTIES ###

    @property
    def confirm(self):
        r'''Is true when confirmation messaging should be displayed.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.confirm
                True

        Returns true or false..
        '''
        return self._confirm

    @property
    def current_score_directory(self):
        r'''Gets current score directory.

        Returns string or none.
        '''
        from ide.tools import idetools
        if self.manifest_current_directory is not None:
            return idetools.AbjadIDE._path_to_score_directory(
                self.manifest_current_directory)

    @property
    def display(self):
        r'''Is true when messaging should be displayed.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.display
                True

        Returns true or false..
        '''
        return self._display

    @property
    def is_in_confirmation_environment(self):
        r'''Is true when session is in confirmation environment.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_confirmation_environment
                False

        Returns true or false..
        '''
        return self._is_in_confirmation_environment

    @property
    def is_in_score(self):
        r'''Is true when session is in score. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_score
                False

        Returns true or false..
        '''
        return self.current_score_directory is not None

    @property
    def is_quitting(self):
        r'''Gets and sets flag that user specified quit.

        ..  container:: example

            ::

                >>> session.is_quitting
                False

        Returns true or false..
        '''
        return self._is_quitting

    @property
    def is_test(self):
        r'''Is true when session is test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_test
                False

        Returns true or false..
        '''
        return self._is_test

    @property
    def last_asset_path(self):
        r'''Gets last material package path.

        Set on package manager entry and persists after package manager exit.

        ..  container:: example

            ::

                >>> session.last_asset_path is None
                True

        Returns string or none.
        '''
        return self._last_asset_path

    @property
    def last_score_path(self):
        r'''Gets last score package path.

        Set on score package manager entry and persists after score package
        manager exit.

        ..  container:: example

            ::

                >>> session.last_score_path is None
                True

        Returns string or none.
        '''
        return self._last_score_path

    @property
    def manifest_current_directory(self):
        r'''Gest manifest current directory.

        Set only by ManifestCurrentDirectory context manager.

        Do not set by hand.
        '''
        return self._manifest_current_directory

    @property
    def pending_input(self):
        r'''Gets and sets pending user input.

        ..  container:: example

            ::

                >>> session.pending_input is None
                True

        Returns string.
        '''
        return self._pending_input

    @property
    def pending_redraw(self):
        r'''Is true when session is pending redraw. Otherwise false.

        ..  container:: example

            ::

                >>> session.pending_redraw
                True

        Returns true or false..
        '''
        return self._pending_redraw