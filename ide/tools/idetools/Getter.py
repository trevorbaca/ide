import abjad
import functools


class Getter(object):
    r'''Getter.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_all_prompts_are_done',
        '_allow_none',
        '_capitalize_prompts',
        '_current_prompt_is_done',
        '_evaluated_input',
        '_include_newlines',
        '_include_chevron',
        '_io_manager',
        '_number_prompts',
        '_prompt_index',
        '_messages',
        '_prompts',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_none=False,
        capitalize_prompts=True,
        include_chevron=True,
        include_newlines=False,
        io_manager=None,
        number_prompts=False,
        ):
        self._prompts = []
        self._allow_none = allow_none
        self._capitalize_prompts = capitalize_prompts
        self._include_chevron = include_chevron
        self._include_newlines = include_newlines
        self._io_manager = io_manager
        self._number_prompts = number_prompts

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format of user input getter.

        Returns string.
        '''
        return repr(self)

    def __len__(self):
        r'''Gets number of prompts in user input getter menu.

        Returns nonnegative integer.
        '''
        return len(self.prompts)

    def __repr__(self):
        r'''Gets interpreter representation of user input getter.

        Returns string.
        '''
        return f'<{type(self).__name__} ({len(self)})>'

    def __str__(self):
        r'''Gets string representation of user input getter.

        Returns string.
        '''
        return repr(self)

    ### PRIVATE METHODS ###

    def _evaluate_input(self, input_, namespace):
        setup_statements = self._get_current_prompt().setup_statements
        if 'evaluated_input' in namespace:
            del(namespace['evaluated_input'])
        if self.allow_none and input_ in ('', 'None'):
            namespace['evaluated_input'] = None
        elif self._get_current_prompt()._is_string:
            namespace['evaluated_input'] = input_
        elif setup_statements:
            for setup_statement in self._get_current_prompt().setup_statements:
                try:
                    command = setup_statement.format(input_)
                    exec(command, namespace, namespace)
                    continue
                except (NameError, SyntaxError):
                    pass
                try:
                    command = setup_statement.format(repr(input_))
                    exec(command, namespace, namespace)
                except ValueError:
                    self.display_help()
        else:
            try:
                input_ = eval(input_, namespace, namespace)
            except (AttributeError, NameError, SyntaxError):
                pass
            namespace['evaluated_input'] = input_
        if 'evaluated_input' not in namespace:
            return
        if not self._validate_evaluated_input(namespace['evaluated_input']):
            self.display_help()
            return
        self._evaluated_input.append(namespace['evaluated_input'])
        self._prompt_index += 1
        self._current_prompt_is_done = True

    def _get_current_prompt(self):
        return self.prompts[self._prompt_index]

    def _indent_and_number_message(self, message):
        if self.number_prompts:
            prompt_number = self._prompt_index + 1
            message = f'({prompt_number}/{len(self)}) {message}'
        return message

    def _load_message(self):
        message = self._get_current_prompt().message
        if self.capitalize_prompts:
            message = abjad.String(message).capitalize_start()
        self._messages.append(message)

    def _make_prompt(
        self,
        spaced_attribute_name,
        disallow_range=False,
        help_template=None,
        help_template_arguments=None,
        include_chevron=True,
        is_string=None,
        setup_statements=None,
        validation_function=None,
        ):
        from ide.tools import idetools
        prompt = idetools.Prompt(
            disallow_range=disallow_range,
            help_template=help_template,
            help_template_arguments=help_template_arguments,
            include_chevron=include_chevron,
            is_string=is_string,
            message=spaced_attribute_name,
            setup_statements=setup_statements,
            validation_function=validation_function,
            )
        self._prompts.append(prompt)

    def _move_to_previous_prompt(self):
        self._evaluated_input.pop()
        self._prompt_index = self._prompt_index - 1

    def _present_prompt(self, include_chevron=True):
        self._load_message()
        self._current_prompt_is_done = False
        namespace = {}
        while not self._current_prompt_is_done:
            message = self._messages[-1]
            message = self._indent_and_number_message(message)
            include_chevron = self._get_current_prompt().include_chevron
            input_ = self._io_manager._handle_input(
                message,
                include_chevron=include_chevron,
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character,
                capitalize_prompt=self.capitalize_prompts,
                )
            if input_ is None:
                self._prompt_index += 1
                break
            elif input_ == '?':
                self.display_help()
                continue
            assert isinstance(input_, str), repr(input_)
            if input_ is None:
                continue
            elif input_ == '<return>':
                self._current_prompt_is_done = True
                self._all_prompts_are_done = True
                self._io_manager._session._pending_redraw = True
            elif input_ is None:
                break
            elif input_ == 'help':
                self.display_help()
            elif input_ == 'previous':
                self._move_to_previous_prompt()
                break
            elif input_ == 'skip':
                break
            elif isinstance(input_, str):
                self._evaluate_input(input_, namespace)
            else:
                message = f'invalid input: {input_!r}.'
                raise ValueError(message)

    def _present_prompts(self, include_chevron=True):
        self._prompt_index = 0
        self._messages = []
        self._evaluated_input = []
        self._all_prompts_are_done = False
        while (self._prompt_index < len(self) and
            not self._all_prompts_are_done):
            self._present_prompt(include_chevron=include_chevron)

    def _run(self, clear_terminal=False, title=False):
        self._present_prompts(include_chevron=self._include_chevron)
        if len(self._evaluated_input) == 1:
            result = self._evaluated_input[0]
        else:
            result = self._evaluated_input[:]
        if result == []:
            result = None
        if result == 'q':
            self._io_manager._session._is_quitting = True
            result = None
        return result

    def _validate_evaluated_input(self, evaluated_input):
        if evaluated_input is None and self.allow_none:
            return True
        validation_function = self._get_current_prompt().validation_function
        try:
            return validation_function(evaluated_input)
        except TypeError:
            return False

    ### PUBLIC PROPERTIES ###

    @property
    def allow_none(self):
        r'''Is true when user input getter allows none.
        Otherwise false.

        Returns true or false.
        '''
        return self._allow_none

    @property
    def capitalize_prompts(self):
        r'''Is true when user input getter capitalizes prompts.
        Otherwise false.

        Returns true or false.
        '''
        return self._capitalize_prompts

    @property
    def include_chevron(self):
        r'''Is true when user input getter incldues chevron.
        Otherwise false.

        Returns true or false.
        '''
        return self._include_chevron

    @property
    def include_newlines(self):
        r'''Is true when user input getter incldues newlines.
        Otherwise false.

        Returns true or false.
        '''
        return self._include_newlines

    @property
    def number_prompts(self):
        r'''Is true when user input getter numbers prompts.
        Otherwise false.

        Returns true or false.
        '''
        return self._number_prompts

    @property
    def prompt_character(self):
        r'''Gets user input getter prompt character.

        Returns string.
        '''
        return ']>'

    @property
    def prompts(self):
        r'''Gets user input getter prompts.

        Returns list of prompts.
        '''
        return self._prompts

    ### PUBLIC METHODS ###

    def append_string(
        self,
        spaced_attribute_name,
        ):
        r'''Appends string.

        Returns prompt.
        '''
        validation_function = Getter.is_string
        help_template = 'value must be string.'
        self._make_prompt(
            spaced_attribute_name,
            is_string=True,
            help_template=help_template,
            validation_function=validation_function,
            )

    def append_yes_no_string(
        self,
        spaced_attribute_name,
        include_chevron=False,
        ):
        r'''Appends yes / no string.

        Returns prompt.
        '''
        help_template = "value for '{}' must be 'y' or 'n'."
        self._make_prompt(
            spaced_attribute_name,
            validation_function=Getter.is_yes_no_string,
            help_template=help_template,
            include_chevron=include_chevron,
            )

    def display_help(self):
        r'''Displays help.

        Returns none.
        '''
        lines = []
        lines.append(self._get_current_prompt().help_string)
        lines.append('')
        self._io_manager._display(lines)

    @staticmethod
    def is_string(argument):
        r'''Predicate.
        '''
        return isinstance(argument, str)

    @staticmethod
    def is_yes_no_string(argument):
        r'''Predicate.
        '''
        return 'yes'.startswith(argument.lower()) or 'no'.startswith(argument.lower())
