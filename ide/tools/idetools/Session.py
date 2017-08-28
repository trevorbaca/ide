class Session(object):
    r'''Session.

        ::

            >>> session = ide.Session()
            >>> session
            Session()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_unknown_command_during_test',
        '_attempted_method',
        '_attempted_to_open_file',
        '_clear_terminal_after_quit',
        '_confirm',
        '_current_directory',
        '_is_example',
        '_is_quitting',
        '_is_test',
        '_pending_input',
        '_pending_menu_rebuild',
        '_pending_redraw',
        '_previous_directory',
        '_previous_input',
        )

    ### INITIALIZER ###

    def __init__(self, input_=None, is_example=False, is_test=False):
        self._allow_unknown_command_during_test = False
        self._attempted_method = None
        self._attempted_to_open_file = False
        self._clear_terminal_after_quit = False
        self._confirm = True
        self._is_example = is_example
        self._is_quitting = False
        self._is_test = is_test
        self._current_directory = None
        self._pending_input = input_
        self._pending_menu_rebuild = False
        self._pending_redraw = True
        self._previous_directory = None
        self._previous_input = None

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
        allow_unknown = self._allow_unknown_command_during_test
        type(self).__init__(
            self,
            is_example=self.is_example,
            is_test=self.is_test,
            )
        self._allow_unknown_command_during_test = allow_unknown

    ### PUBLIC PROPERTIES ###

    @property
    def current_directory(self):
        r'''Gets manifest current directory.

        Returns string.
        '''
        return self._current_directory

    @property
    def is_example(self):
        r'''Is true when session is example. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_example
                False

        Returns true or false.
        '''
        return self._is_example

    @property
    def is_quitting(self):
        r'''Gets and sets flag that user specified quit.

        ..  container:: example

            ::

                >>> session.is_quitting
                False

        Returns true or false.
        '''
        return self._is_quitting

    @property
    def is_test(self):
        r'''Is true when session is test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_test
                False

        Returns true or false.
        '''
        return self._is_test

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

        Returns true or false.
        '''
        return self._pending_redraw

    @property
    def previous_directory(self):
        r'''Gets previous directory.

        Returns directory.
        '''
        return self._previous_directory

    @property
    def previous_input(self):
        r'''Gets previous input.

        Returns string or none.
        '''
        return self._previous_input
