# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import abctools
from abjad.tools import stringtools
from abjad.tools import systemtools


class Session(abctools.AbjadObject):
    r'''Abjad IDE session.

    ..  container:: example

        Session outside of score:

        ::

            >>> session = ide.idetools.Session()
            >>> session
            Session()

    ..  container:: example

        Session in score:

        ::

            >>> session_in_score = ide.idetools.Session()
            >>> session_in_score._set_test_score('red_example_score')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abjad_ide',
        '_aliases',
        '_allow_unknown_command_during_test',
        '_after_redraw_message',
        '_attempted_display_status',
        '_attempted_remove_unadded_assets',
        '_attempted_to_add',
        '_attempted_to_commit',
        '_attempted_to_open_file',
        '_attempted_to_remove',
        '_attempted_to_revert',
        '_attempted_to_update',
        '_clear_terminal_after_quit',
        '_command_history',
        '_confirm',
        '_configuration',
        '_controller_stack',
        '_current_score_directory',
        '_display',
        '_display_available_commands',
        '_initial_input',
        '_io_manager',
        '_is_backtracking_locally',
        '_is_backtracking_to_all_build_files',
        '_is_navigating_home',
        '_is_backtracking_to_score',
        '_is_navigating_to_scores',
        '_is_in_confirmation_environment',
        '_is_in_user_input_getter',
        '_is_navigating_to_build_files',
        '_is_navigating_to_distribution_files',
        '_is_navigating_to_etc_files',
        '_is_navigating_to_next_asset',
        '_is_navigating_to_next_score',
        '_is_navigating_to_previous_asset',
        '_is_navigating_to_previous_score',
        '_is_navigating_to_maker_files',
        '_is_navigating_to_materials',
        '_is_navigating_to_segments',
        '_is_navigating_to_stylesheets',
        '_is_quitting',
        '_is_repository_test',
        '_is_test',
        '_last_asset_path',
        '_last_command_was_composite',
        '_last_score_path',
        '_pending_done',
        '_pending_input',
        '_pending_redraw',
        '_transcript',
        )

    ### INITIALIZER ###

    def __init__(self, input_=None, is_test=False):
        from ide import idetools
        self._abjad_ide = None
        self._aliases = {}
        self._after_redraw_message = None
        self._allow_unknown_command_during_test = False
        self._attempted_display_status = False
        self._attempted_remove_unadded_assets = False
        self._attempted_to_add = False
        self._attempted_to_commit = False
        self._attempted_to_open_file = False
        self._attempted_to_remove = False
        self._attempted_to_revert = False
        self._attempted_to_update = False
        self._clear_terminal_after_quit = False
        self._command_history = []
        self._configuration = idetools.Configuration()
        self._confirm = True
        self._controller_stack = []
        self._current_score_directory = None
        self._display = True
        self._display_available_commands = False
        self._initial_input = input_
        self._io_manager = idetools.IOManager(session=self)
        self._is_backtracking_locally = False
        self._is_backtracking_to_all_build_files = False
        self._is_navigating_home = False
        self._is_backtracking_to_score = False
        self._is_navigating_to_scores = False
        self._is_in_confirmation_environment = False
        self._is_navigating_to_build_files = False
        self._is_navigating_to_distribution_files = False
        self._is_navigating_to_etc_files = False
        self._is_navigating_to_next_asset = False
        self._is_navigating_to_next_score = False
        self._is_navigating_to_previous_asset = False
        self._is_navigating_to_previous_score = False
        self._is_navigating_to_maker_files = False
        self._is_navigating_to_materials = False
        self._is_navigating_to_segments = False
        self._is_navigating_to_stylesheets = False
        self._is_quitting = False
        self._is_repository_test = False
        self._is_test = is_test
        self._last_asset_path = None
        self._last_command_was_composite = False
        self._last_score_path = None
        self._pending_done = False
        self._pending_input = input_
        self._pending_redraw = True
        self._transcript = idetools.Transcript()

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
        if self.initial_input is not None:
            string = 'initial_input_={!r}'
            string = string.format(self.initial_input)
            summary.append(string)
        if self.pending_input not in (None, ''):
            string = 'input_={!r}'
            string = string.format(self.pending_input)
            summary.append(string)
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    ### PRIVATE METHODS ###

    def _clean_up(self):
        if self.is_test:
            return
        transcripts_directory = self._configuration.transcripts_directory
        transcripts = sorted(os.listdir(transcripts_directory))
        count = len(transcripts)
        if 9000 <= count:
            messages = []
            message = 'transcripts directory contains {} transcripts.'
            message = message.format(count)
            messages.append(message)
            message = 'prune {} soon.'.format(transcripts_directory)
            messages.append(message)
            self.io_manager._display(messages)
        self.transcript._write()

    def _format_controller_breadcrumbs(self, stop_controller=None):
        from ide import idetools
        if not self.controller_stack:
            return ['']
        result_lines = []
        first_controller = self.controller_stack[0]
        breadcrumb = getattr(first_controller, 'breadcrumb', None)
        breadcrumb = breadcrumb or first_controller._breadcrumb
        if breadcrumb:
            result_lines.append(breadcrumb)
        for controller in self.controller_stack[1:]:
            if controller is stop_controller:
                break
            if isinstance(controller, idetools.Selector):
                continue
            breadcrumb = getattr(controller, 'breadcrumb', None)
            breadcrumb = breadcrumb or controller._breadcrumb
            if not breadcrumb:
                continue
            if result_lines:
                candidate_line = result_lines[-1] + ' - ' + breadcrumb
            else:
                candidate_line = breadcrumb
            if result_lines:
                result_lines[-1] = candidate_line
            else:
                result_lines.append(candidate_line)
        return result_lines

    def _make_menu_header(self, annotate_edit=True, stop_controller=None):
        breadcrumbs = self._format_controller_breadcrumbs(
            stop_controller=stop_controller,
            )
        header = '\n'.join(breadcrumbs)
        if header == 'Abjad IDE':
            header = 'Abjad IDE - home'
        return header

    def _print_transcript(self):
        for entry in self.transcript:
            print(entry)

    def _print_transcript_titles(self):
        for title in self.transcript.titles:
            print(repr(title))

    def _reinitialize(self):
        is_test = self._is_test
        is_add_test = self._is_repository_test
        allow_unknown = self._allow_unknown_command_during_test
        type(self).__init__(self, is_test=self.is_test)
        self._is_repository_test = is_add_test
        self._allow_unknown_command_during_test = allow_unknown

    def _set_test_score(self, score_package_name):
        from ide import idetools
        assert not self.controller_stack
        path = os.path.join(
            self._configuration.example_score_packages_directory,
            score_package_name,
            )
        assert os.path.exists(path)
        manager = idetools.ScorePackageManager(
            path=path,
            session=self,
            )
        self._controller_stack.append(manager)

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_ide(self):
        r'''Gets session IDE.

        ..  container:: example

            ::

                >>> session.abjad_ide

        Returns Abjad IDE or none.
        '''
        return self._abjad_ide

    @property
    @systemtools.Memoize
    def aliases(self):
        r'''Gets session aliases.

        ..  container:: example

            ::

                >>> session.aliases
                OrderedDict(...)

        Returns ordered dictionary.
        '''
        aliases = None
        aliases_file_path = self._configuration.aliases_file_path
        if os.path.isfile(aliases_file_path):
            with open(aliases_file_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            try:
                result = self._io_manager.execute_string(
                    file_contents_string,
                    attribute_names=('aliases',),
                    )
                aliases = result[0]
            except SyntaxError:
                message = 'syntax error in file: {!r}.'
                message = message.format(aliases_file_path)
                self._io_manager._display(message)
        aliases = aliases or collections.OrderedDict()
        return aliases

    @property
    def command_history(self):
        r'''Gets session command history.

        ..  container:: example

            ::

                >>> session.command_history
                []

        Returns list.
        '''
        return self._command_history

    @property
    def command_history_string(self):
        r'''Gets session command history string.

        ..  container:: example

            ::

                >>> session.command_history_string
                ''

        Returns string.
        '''
        return ' '.join(self.explicit_command_history)

    @property
    def confirm(self):
        r'''Is true when confirmation messaging should be displayed.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.confirm
                True

        Returns boolean.
        '''
        return self._confirm

    @property
    def controller_stack(self):
        r'''Gets session controller stack.

        ..  container:: example

            ::

                >>> session.controller_stack
                []

        Returns list of objects all of which are either wranglers or idetools.
        '''
        return self._controller_stack

    @property
    def current_abbreviations_file_path(self):
        r'''Gets current abbreviations file path.

        ..  container:: example

            ::

                >>> session.current_abbreviations_file_path is None
                True

        Returns string or none.
        '''
        if self.is_in_score:
            return os.path.join(
                self.current_score_directory,
                'materials',
                '__abbreviations__.py',
                )

    @property
    def current_build_directory(self):
        r'''Gets session current build directory.

        ..  container:: example

            Build directory of session outside score:

            ::

                >>> session.current_build_directory is None
                True

        ..  container:: example

            Build directory of session in score:

            ::

                >>> session_in_score.current_build_directory
                '.../red_example_score/build'

        Returns string.
        '''
        if self.current_score_directory:
            return os.path.join(self.current_score_directory, 'build')

    @property
    def current_controller(self):
        r'''Gets current controller of session.

        ..  container:: example

            ::

                >>> session.current_controller is None
                True

        Returns wrangler or manager.
        '''
        if self.controller_stack:
            return self.controller_stack[-1]

    @property
    def current_distribution_directory(self):
        r'''Gets session current distribution directory.

        ..  container:: example

            Distribution directory of session outside score:

            ::

                >>> session.current_distribution_directory is None
                True

        ..  container:: example

            Materials directory of session in score:

            ::

                >>> session_in_score.current_distribution_directory
                '.../red_example_score/distribution'

        Returns string.
        '''
        if self.current_score_directory:
            return os.path.join(self.current_score_directory, 'distribution')

    @property
    def current_etc_directory(self):
        r'''Gets session current etc directory.

        ..  container:: example

            Etc directory of session outside score:

            ::

                >>> session.current_etc_directory is None
                True

        ..  container:: example

            Etc directory of session in score:

            ::

                >>> session_in_score.current_etc_directory
                '.../red_example_score/etc'

        Returns string.
        '''
        if self.current_score_directory:
            return os.path.join(self.current_score_directory, 'etc')
            
    @property
    def current_materials_directory(self):
        r'''Gets session current materials directory.

        ..  container:: example

            Materials directory of session outside score:

            ::

                >>> session.current_materials_directory is None
                True

        ..  container:: example

            Materials directory of session in score:

            ::

                >>> session_in_score.current_materials_directory
                '.../red_example_score/materials'

        Returns string.
        '''
        if self.current_score_directory:
            return os.path.join(self.current_score_directory, 'materials')

    @property
    def current_score_directory(self):
        r'''Gets session current score directory.

        ..  container:: example

            ::

                >>> session.current_score_directory is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_directory
                '.../red_example_score'

        Returns string or none.
        '''
        if self._current_score_directory:
            return self._current_score_directory
        elif self.current_score_package_manager:
            return self.current_score_package_manager._path

    @property
    def current_score_package_manager(self):
        r'''Gets session current score package manager.

        ..  container:: example:

            ::

                >>> session.current_score_package_manager is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_package_manager
                ScorePackageManager('.../red_example_score')

        (Ouput will vary according to configuration.)

        Returns score package manager or none.
        '''
        from ide import idetools
        for controller in reversed(self.controller_stack):
            if isinstance(controller, idetools.ScorePackageManager):
                return controller

    @property
    def current_score_package_name(self):
        r'''Gets session current score package name.

        ..  container:: example

            Score package name of session outside score:

            ::

                >>> session.current_score_package_name is None
                True

        ..  container:: example

            Score package nmae of session in score:

            ::

                >>> session_in_score.current_score_package_name
                'red_example_score'

        Returns string.
        '''
        if self.current_score_directory:
            return os.path.basename(self.current_score_directory)

    @property
    def current_segments_directory(self):
        r'''Gets session current segments directory.

        ..  container:: example

            ::

                >>> session.current_segments_directory is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_segments_directory
                '.../red_example_score/segments'

        Returns string.
        '''
        if self.current_score_directory:
            return os.path.join(self.current_score_directory, 'segments')

    @property
    def current_stylesheet_path(self):
        r'''Gets session current stylesheet path.

        ..  container::

            ::

                >>> session.current_stylesheet_path is None
                True

        Returns string or none.
        '''
        if self.is_in_score:
            return os.path.join(
                self.current_score_directory,
                'stylesheets',
                'stylesheet.ily',
                )

    @property
    def display(self):
        r'''Is true when messaging should be displayed.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.display
                True

        Returns boolean.
        '''
        return self._display

    @property
    def display_available_commands(self):
        r'''Is true when available commands will display. Otherwise false.

        ..  container:: example

            ::

                >>> session.display_available_commands
                False

        Returns boolean.
        '''
        return self._display_available_commands

    @property
    def explicit_command_history(self):
        r'''Gets session explicit command history.

        ..  container:: example

            ::

                >>> session.explicit_command_history
                []

        Returns list.
        '''
        result = []
        for command in self.command_history:
            if command == '':
                result.append('<return>')
            else:
                result.append(command)
        return result

    @property
    def initial_input(self):
        r'''Gets session initial user input.

        ..  container:: example

            ::

                >>> session.initial_input is None
                True

        Returns string or none.
        '''
        return self._initial_input

    @property
    def io_manager(self):
        r'''Gets session IO manager.

        ..  container:: example

            ::

                >>> session.io_manager
                IOManager()

        Returns IO manager.
        '''
        return self._io_manager

    @property
    def is_at_top_level(self):
        r'''Is true when IDE is at top level. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_at_top_level
                True

        Returns boolean.
        '''
        from ide import idetools
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

        Returns boolean.
        '''
        return self.wrangler_navigation_directive is not None

    @property
    def is_backtracking(self):
        r'''Is true when any of the following are true:

        ..  container:: example

            ::

                >>> session.is_backtracking
                False

        Returns boolean.
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

        Returns boolean.
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

        Returns boolean.
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

        Returns boolean.
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

        Returns boolean.
        '''
        return self._is_in_confirmation_environment

    @property
    def is_in_score(self):
        r'''Is true when session is in score. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_score
                False

        Returns boolean.
        '''
        if self.current_score_package_manager is not None:
            return True
        return False

    @property
    def is_in_user_input_getter(self):
        r'''Is true when session is in user input getter. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_user_input_getter
                False

        Returns boolean.
        '''
        from ide import idetools
        for controller in reversed(self.controller_stack):
            if isinstance(controller, idetools.Getter):
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

        Returns boolean.
        '''
        return self._is_navigating_home

    @property
    def is_navigating_to_build_files(self):
        r'''Is true when session is navigating to build directory.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_build_files
                False

        Returns boolean.
        '''
        return self._is_navigating_to_build_files

    @property
    def is_navigating_to_distribution_files(self):
        r'''Is true when session is navigating to distribution directory.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_distribution_files
                False

        Returns boolean.
        '''
        return self._is_navigating_to_distribution_files

    @property
    def is_navigating_to_etc_files(self):
        r'''Is true when session is navigating to etc directory.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_etc_files
                False

        Returns boolean.
        '''
        return self._is_navigating_to_etc_files

    @property
    def is_navigating_to_maker_files(self):
        r'''Is true when session is navigating to score makers.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_maker_files
                False

        Returns boolean.
        '''
        return self._is_navigating_to_maker_files

    @property
    def is_navigating_to_materials(self):
        r'''Is true when session is navigating to score materials.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_materials
                False

        Returns boolean.
        '''
        return self._is_navigating_to_materials

    @property
    def is_navigating_to_next_asset(self):
        r'''Is true when session is navigating to next material.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_asset
                False

        Returns boolean.
        '''
        return self._is_navigating_to_next_asset

    @property
    def is_navigating_to_next_score(self):
        r'''Is true when session is navigating to next score. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_score
                False

        Returns boolean.
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

        Returns boolean.
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

        Returns boolean.
        '''
        return self._is_navigating_to_previous_score

    @property
    def is_navigating_to_segments(self):
        r'''Is true when session is navigating to score segments.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_segments
                False

        Returns boolean.
        '''
        return self._is_navigating_to_segments

    @property
    def is_navigating_to_sibling_asset(self):
        r'''Is true when session is navigating to sibling asset.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_navigating_to_sibling_asset
                False

        Returns boolean.
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

        Returns boolean.
        '''
        if self.is_navigating_to_next_score:
            return True
        if self.is_navigating_to_previous_score:
            return True
        return False

    @property
    def is_navigating_to_stylesheets(self):
        r'''Is true when session is navigating to score stylesheets.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_stylesheets
                False

        Returns boolean.
        '''
        return self._is_navigating_to_stylesheets

    @property
    def is_quitting(self):
        r'''Gets and sets flag that user specified quit.

        ..  container:: example

            ::

                >>> session.is_quitting
                False

        Returns boolean.
        '''
        return self._is_quitting

    @property
    def is_repository_test(self):
        r'''Is true when session is repository test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_repository_test
                False

        Returns boolean.
        '''
        return self._is_repository_test

    @property
    def is_test(self):
        r'''Is true when session is test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_test
                False

        Returns boolean.
        '''
        return self._is_test

    @property
    def last_asset_path(self):
        r'''Gets last material package path.

        Set on package manager entry and persists
        after package manager exit.

        ..  container:: example

            ::

                >>> session.last_asset_path is None
                True

        Returns string or none.
        '''
        return self._last_asset_path

    @property
    def last_command_was_composite(self):
        r'''Is true when last command was composite. Otherwise false.

        ..  container:: example

            ::

                >>> session.last_command_was_composite
                False

        Returns boolean.
        '''
        return self._last_command_was_composite

    @property
    def last_score_path(self):
        r'''Gets last score package path.

        Set on score package manager entry and persists
        after score package manager exit.

        ..  container:: example

            ::

                >>> session.last_score_path is None
                True

        Returns string or none.
        '''
        return self._last_score_path

    @property
    def last_semantic_command(self):
        r'''Gets session last semantic command.

        ..  container:: example

            ::

                >>> session.last_semantic_command is None
                True

        Returns string or none.
        '''
        for command in reversed(self.command_history):
            if not command.startswith('.'):
                return command

    @property
    def menu_header(self):
        r'''Gets session menu header.

        ..  container:: example

            ::

                >>> session.menu_header
                ''

        Returns string.
        '''
        return self._make_menu_header()

    @property
    def pending_done(self):
        r'''Is true when something is pending done. Otherwise false.

        ..  container:: example

            ::

                >>> session.pending_done
                False

        Returns boolean.
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

        Returns boolean.
        '''
        return self._pending_redraw

    @property
    def testable_command_history_string(self):
        r'''Gets session testable command history string.

        ..  container:: example

            ::

                >>> session.testable_command_history_string
                ''

        Returns string.
        '''
        result = []
        for part in self.explicit_command_history:
            if ' ' in part and ',' not in part:
                part = part.replace(' ', '~')
            result.append(part)
        return ' '.join(result)

    @property
    def transcript(self):
        r'''Gets session IO transcript.

        ..  container:: example

            ::

                >>> session.transcript
                Transcript()

        Returns IO transcript.
        '''
        return self._transcript

    @property
    def wrangler_navigation_directive(self):
        r'''Gets wrangler navigation directive.

        ..  container:: example

            ::

                >>> session.wrangler_navigation_directive is None
                True

        Returns u, d, k, m, g, y or none.
        '''
        if self.is_navigating_to_build_files:
            return 'u'
        elif self.is_navigating_to_distribution_files:
            return 'd'
        elif self.is_navigating_to_etc_files:
            return 'e'
        elif self.is_navigating_to_maker_files:
            return 'k'
        elif self.is_navigating_to_materials:
            return 'm'
        elif self.is_navigating_to_segments:
            return 'g'
        elif self.is_navigating_to_stylesheets:
            return 'y'