# -*- encoding: utf-8 -*-


class Session(object):
    r'''Abjad IDE session.

    ..  container:: example

        Session outside of score:

        ::

            >>> session = ide.tools.idetools.Session()
            >>> session
            Session()

    ..  container:: example

        Session in score:

        ::

            >>> session_in_score = ide.tools.idetools.Session()
            >>> session_in_score
            Session()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_unknown_command_during_test',
        '_after_redraw_message',
        '_attempted_display_status',
        '_attempted_to_add',
        '_attempted_to_commit',
        '_attempted_to_open_file',
        '_attempted_to_remove',
        '_attempted_to_revert',
        '_attempted_to_update',
        '_clear_terminal_after_quit',
        '_confirm',
        '_controller_stack',
        '_current_score_directory',
        '_display',
        '_display_command_help',
        '_is_backtracking_locally',
        '_is_backtracking_to_all_build_files',
        '_is_backtracking_to_score',
        '_is_navigating_home',
        '_is_in_confirmation_environment',
        '_is_navigating_to_next_asset',
        '_is_navigating_to_next_score',
        '_is_navigating_to_previous_asset',
        '_is_navigating_to_previous_score',
        '_is_navigating_to_scores',
        '_is_quitting',
        '_is_repository_test',
        '_is_test',
        '_last_asset_path',
        '_last_score_path',
        '_manifest_current_directory',
        '_navigation_target',
        '_pending_done',
        '_pending_input',
        '_pending_redraw',
        )

    ### INITIALIZER ###

    def __init__(self, input_=None, is_test=False):
        from ide.tools import idetools
        self._after_redraw_message = None
        self._allow_unknown_command_during_test = False
        self._attempted_display_status = False
        self._attempted_to_add = False
        self._attempted_to_commit = False
        self._attempted_to_open_file = False
        self._attempted_to_remove = False
        self._attempted_to_revert = False
        self._attempted_to_update = False
        self._clear_terminal_after_quit = False
        self._confirm = True
        self._controller_stack = []
        self._current_score_directory = None
        self._display = True
        self._display_command_help = None
        self._is_backtracking_locally = False
        self._is_backtracking_to_all_build_files = False
        self._is_backtracking_to_score = False
        self._is_in_confirmation_environment = False
        self._is_navigating_home = False
        self._is_navigating_to_next_asset = False
        self._is_navigating_to_next_score = False
        self._is_navigating_to_previous_asset = False
        self._is_navigating_to_previous_score = False
        self._is_navigating_to_scores = False
        self._is_quitting = False
        self._is_repository_test = False
        self._is_test = is_test
        self._last_asset_path = None
        self._last_score_path = None
        self._manifest_current_directory = None
        self._navigation_target = None
        self._pending_done = False
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
        is_add_test = self._is_repository_test
        allow_unknown = self._allow_unknown_command_during_test
        type(self).__init__(self, is_test=self.is_test)
        self._is_repository_test = is_add_test
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
    def controller_stack(self):
        r'''Gets controller stack.

        ..  container:: example

            ::

                >>> session.controller_stack
                []

        Returns list of objects all of which are either wranglers or idetools.
        '''
        from ide.tools import idetools
        if 1 <= len(self._controller_stack):
            first_controller = self._controller_stack[0]
            assert isinstance(first_controller, idetools.AbjadIDE), repr(
                first_controller)
        return self._controller_stack

    @property
    def current_score_directory(self):
        r'''Gets current score directory.

        ..  container:: example

            ::

                >>> session.current_score_directory is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_directory is None
                True

        Returns string or none.
        '''
        if self.current_score_package_manager:
            return self.current_score_package_manager._path

    @property
    def current_score_package_manager(self):
        r'''Gets current score package manager.

        ..  container:: example:

            ::

                >>> session.current_score_package_manager is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_package_manager is None
                True

        Returns package manager or none.
        '''
        for controller in self.controller_stack:
            if hasattr(controller, '_path'):
                return controller

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
    def display_command_help(self):
        r'''Is true when either action commands or navigation commands will
        display. Otherwise false.

        ..  container:: example

            ::

                >>> session.display_command_help is None
                True

        Returns 'action', 'navigation' or none.
        '''
        return self._display_command_help

    @property
    def is_at_top_level(self):
        r'''Is true when IDE is at top level. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_at_top_level
                True

        Returns true or false..
        '''
        from ide.tools import idetools
        for controller in self.controller_stack:
            if isinstance(controller, idetools.Wrangler):
                return False
        return True

    @property
    def is_autonavigating_within_score(self):
        r'''Is true when session is autonavigating. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_autonavigating_within_score
                False

        Returns true or false..
        '''
        return self.navigation_target is not None

    @property
    def is_backtracking(self):
        r'''Is true when any of the following are true:

        ..  container:: example

            ::

                >>> session.is_backtracking
                False

        Returns true or false..
        '''
        if (
            self.is_autonavigating_within_score or
            self.is_backtracking_locally or 
            self.is_backtracking_to_all_scores or
            self.is_backtracking_to_score or
            self.is_quitting
            ):
            return True
        if self.is_navigating_home and not self.is_at_top_level:
            return True
        return False

    @property
    def is_backtracking_locally(self):
        r'''Is true when session is backtracking locally.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_backtracking_locally
                False

        Returns true or false..
        '''
        return self._is_backtracking_locally

    @property
    def is_backtracking_to_all_scores(self):
        r'''Is true when session is backtracking to Abjad IDE.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_backtracking_to_all_scores
                False

        Returns true or false..
        '''
        return self._is_navigating_to_scores

    @property
    def is_backtracking_to_score(self):
        r'''Is true when session is backtracking to score.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_backtracking_to_score
                False

        Returns true or false..
        '''
        return self._is_backtracking_to_score

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
        if self.current_score_package_manager is not None:
            return True
        return False

    @property
    def is_navigating_home(self):
        r'''Is true when session is navigating home.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_home
                False

        Returns true or false..
        '''
        return self._is_navigating_home

    @property
    def is_navigating_to_next_asset(self):
        r'''Is true when session is navigating to next material.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_asset
                False

        Returns true or false..
        '''
        return self._is_navigating_to_next_asset

    @property
    def is_navigating_to_next_score(self):
        r'''Is true when session is navigating to next score. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_score
                False

        Returns true or false..
        '''
        return self._is_navigating_to_next_score

    @property
    def is_navigating_to_previous_asset(self):
        r'''Is true when session is navigating to previous material.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_previous_asset
                False

        Returns true or false..
        '''
        return self._is_navigating_to_previous_asset

    @property
    def is_navigating_to_previous_score(self):
        r'''Is true when session is navigating to previous score.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_previous_score
                False

        Returns true or false..
        '''
        return self._is_navigating_to_previous_score

    @property
    def is_navigating_to_sibling_asset(self):
        r'''Is true when session is navigating to sibling asset.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_navigating_to_sibling_asset
                False

        Returns true or false..
        '''
        if self.is_navigating_to_next_asset:
            return True
        if self.is_navigating_to_previous_asset:
            return True
        return False

    @property
    def is_navigating_to_sibling_score(self):
        r'''Is true when session is navigating to sibling score.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_navigating_to_sibling_score
                False

        Returns true or false..
        '''
        if self.is_navigating_to_next_score:
            return True
        if self.is_navigating_to_previous_score:
            return True
        return False

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
    def is_repository_test(self):
        r'''Is true when session is repository test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_repository_test
                False

        Returns true or false..
        '''
        return self._is_repository_test

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

        Set only by CurrentDirectory context manager.

        Do not set by hand.
        '''
        return self._manifest_current_directory

    @property
    def navigation_target(self):
        r'''Gets navigation target.

        ..  container:: example

            ::

                >>> session.navigation_target is None
                True

        Returns 'build', 'distribution', 'etc', 'makers', 'stylesheets',
        'segments', 'materials' or none.
        '''
        return self._navigation_target

    @property
    def pending_done(self):
        r'''Is true when something is pending done. Otherwise false.

        ..  container:: example

            ::

                >>> session.pending_done
                False

        Returns true or false..
        '''
        return self._pending_done

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