# -*- encoding: utf-8 -*-
import re
import functools
import numbers
from abjad import *
from abjad.tools.abctools.AbjadObject import AbjadObject


class PromptMakerMixin(AbjadObject):
    r'''Prompt maker mixin.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    ### PRIVATE METHODS ###

    def _make_prompt(
        self,
        spaced_attribute_name,
        disallow_range=False,
        help_template=None,
        help_template_arguments=None,
        include_chevron=True,
        setup_statements=None,
        target_menu_section=None,
        validation_function=None,
        ):
        from ide.tools import idetools
        prompt = idetools.Prompt(
            disallow_range=disallow_range,
            help_template=help_template,
            help_template_arguments=help_template_arguments,
            include_chevron=include_chevron,
            message=spaced_attribute_name,
            setup_statements=setup_statements,
            target_menu_section=target_menu_section,
            validation_function=validation_function,
            )
        self._prompts.append(prompt)

    ### PUBLIC METHODS ###

    def append_articulation(
        self,
        spaced_attribute_name,
        ):
        r'''Appends articulation.

        Returns prompt.
        '''
        help_template = 'value'
        help_template += ' must successfully initialize articulation.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_articulation_token,
            help_template=help_template,
            )

    def append_articulations(
        self,
        spaced_attribute_name,
        ):
        r'''Appends articulations.

        Returns prompt.
        '''
        help_template = 'value '
        help_template += ' must successfully initialize articulations.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.are_articulation_tokens,
            help_template=help_template,
            )

    def append_available_snake_case_package_name(
        self,
        spaced_attribute_name,
        ):
        r'''Appends available snake case package name.

        Returns prompt.
        '''
        help_template = 'value must be available '
        help_template += 'underscore-delimited lowercase package name.'
        validation_function = PromptMakerMixin.is_available_snake_case_package_name
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            )

    def append_boolean(
        self,
        spaced_attribute_name,
        ):
        r'''Appends boolean.

        Returns prompt.
        '''
        help_template = 'value must be boolean.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_boolean,
            help_template=help_template,
            )

    def append_clef(
        self,
        spaced_attribute_name,
        ):
        r'''Appends clef.

        Returns prompt.
        '''
        help_template = 'value'
        help_template += ' must successfully initialize clef.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_clef_token,
            help_template=help_template,
            )

    def append_constellation_circuit_id_pair(
        self,
        spaced_attribute_name,
        ):
        r'''Appends constellation circuit ID pair.

        Returns prompt.
        '''
        help_template = 'value must be valid constellation circuit id pair.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=lambda x: True,
            help_template=help_template,
            )

    def append_dash_case_file_name(
        self,
        spaced_attribute_name,
        ):
        r'''Appends dash case file name.

        Returns prompt.
        '''
        help_template = 'value must be dash case file name.'
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=stringtools.is_dash_case_file_name,
            )

    def append_direction_string(
        self,
        spaced_attribute_name,
        ):
        r'''Appends direction string.

        Returns prompt.
        '''
        help_template = "value must be 'up or 'down'."
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=PromptMakerMixin.is_direction_string,
            )

    def append_duration(
        self,
        spaced_attribute_name,
        ):
        r'''Appends duration.

        Returns prompt.
        '''
        help_template = 'value must be duration.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        setup_statements.append('evaluated_input = Duration({})')
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_duration_token,
            help_template=help_template,
            setup_statements=setup_statements,
            )

    def append_durations(
        self,
        spaced_attribute_name,
        ):
        r'''Appends durations.

        Returns prompt.
        '''
        help_template = 'value must be list of durations.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        setup_statements.append('evaluated_input = [Duration(x) for x in {}]')
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.are_duration_tokens,
            help_template=help_template,
            setup_statements=setup_statements,
            )

    def append_dynamic(
        self,
        spaced_attribute_name,
        ):
        r'''Appends dynamic.

        Returns prompt.
        '''
        help_template = 'value'
        help_template += ' must successfully initialize dynamic.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_dynamic_token,
            help_template=help_template,
            )

    def append_dynamics(
        self,
        spaced_attribute_name,
        ):
        r'''Appends dynamics.

        Returns prompt.
        '''
        help_template = 'value must be list of dynamic initializers.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.are_dynamic_tokens,
            help_template=help_template,
            )

    def append_existing_package_name(
        self,
        spaced_attribute_name,
        ):
        r'''Appends existing package name.

        Returns prompt.
        '''
        help_template = 'value must be existing package name.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_existing_package_name,
            help_template=help_template,
            )

    def append_expr(
        self,
        spaced_attribute_name,
        ):
        r'''Appends expression.

        Returns prompt.
        '''
        help_template = 'value may be anything.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=lambda expr: True,
            help_template=help_template,
            )

    def append_hairpin_token(
        self,
        spaced_attribute_name,
        ):
        r'''Appends hairpin token.

        Returns prompt.
        '''
        help_template = 'value must be hairpin token.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_hairpin_token,
            help_template=help_template,
            )

    def append_hairpin_tokens(
        self,
        spaced_attribute_name,
        ):
        r'''Appends hairpin tokens.

        Returns prompt.
        '''
        help_template = 'value must be tuple of hairpin tokens.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.are_hairpin_tokens,
            help_template=help_template,
            )

    def append_identifier(
        self,
        spaced_attribute_name,
        allow_spaces=False,
        ):
        r'''Appends Python identifier.

        String beginning with a letter or underscore and containing only 
        letters, digits and underscores.

        Returns prompt.
        '''
        help_template = 'value must be valid Python identifier.'
        helper = lambda x: PromptMakerMixin.is_identifier(
            x, allow_spaces=allow_spaces)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=helper,
            help_template=help_template,
            )

    def append_integer(
        self,
        spaced_attribute_name,
        ):
        r'''Appends integer.

        Returns prompt.
        '''
        help_template = 'value must be integer.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_integer,
            help_template=help_template,
            )

    def append_integer_in_range(
        self,
        spaced_attribute_name,
        start=None,
        stop=None,
        allow_none=False,
        ):
        r'''Appends integer in range.

        Returns prompt.
        '''
        validation_function = functools.partial(
            PromptMakerMixin.is_integer_in_range,
            start=start,
            stop=stop,
            allow_none=allow_none,
            )
        help_template = 'value must be integer between {} and {}, inclusive.'
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=validation_function,
            help_template_arguments=(start, stop),
            )

    def append_integers(
        self,
        spaced_attribute_name,
        ):
        r'''Appends integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of integers.'
        function = lambda x: all(PromptMakerMixin.is_integer(y) for y in x)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            )

    def append_list(
        self,
        spaced_attribute_name,
        ):
        r'''Appends lists.

        Returns prompt.
        '''
        help_template = 'value must be list.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_list,
            help_template=help_template,
            )

    def append_lists(
        self,
        spaced_attribute_name,
        ):
        r'''Appends lists.

        Returns prompt.
        '''
        help_template = 'value must be tuple of lists.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.are_lists,
            help_template=help_template,
            )

    def append_markup(
        self,
        spaced_attribute_name,
        ):
        r'''Appends markup.

        Returns prompt.
        '''
        help_template = 'value must be markup.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        statement = 'evaluated_input = markuptools.Markup({})'
        setup_statements.append(statement)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_markup,
            help_template=help_template,
            setup_statements=setup_statements,
            )

    def append_menu_section_item(
        self,
        spaced_attribute_name,
        target_menu_section,
        ):
        r'''Appends menu section item.

        Returns prompt.
        '''
        help_template = 'value must be menu section item.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_list,
            help_template=help_template,
            target_menu_section=target_menu_section,
            disallow_range=True,
            )

    def append_menu_section_range(
        self,
        spaced_attribute_name,
        target_menu_section,
        ):
        r'''Appends menu section range.

        Returns prompt.
        '''
        help_template = 'value must be argument range.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_list,
            help_template=help_template,
            target_menu_section=target_menu_section,
            )

    def append_named_pitch(
        self,
        spaced_attribute_name,
        ):
        r'''Appends named pitch.

        Returns prompt.
        '''
        help_template = 'value must be named pitch.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        string = 'evaluated_input = pitchtools.NamedPitch({!r})'
        setup_statements.append(string)
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=PromptMakerMixin.is_named_pitch,
            setup_statements=setup_statements,
            )

    def append_nonnegative_integer(
        self,
        spaced_attribute_name,
        ):
        r'''Appends nonnegative integer.

        Returns prompt.
        '''
        help_template = 'value must be nonnegative integer.'
        function = lambda x: 0 < x
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            )

    def append_nonnegative_integers(
        self,
        spaced_attribute_name,
        ):
        r'''Appends nonnegative integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of nonnegative integers.'
        function = lambda x: all(isinstance(y, int) and 0 <= y for y in x)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            )

    def append_nonzero_integers(
        self,
        spaced_attribute_name,
        ):
        r'''Appends nonzero integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of nonzero integers.'
        function = lambda x: all(isinstance(y, int) and not y == 0 for y in x)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            )

    def append_number(
        self,
        spaced_attribute_name,
        ):
        r'''Appends number.

        Returns prompt.
        '''
        help_template = 'value must be number.'
        function = lambda x: isinstance(x, numbers.Number)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            )

    def append_paper_dimensions(
        self,
        spaced_attribute_name,
        ):
        r'''Appends paper dimensions.

        Returns prompt.
        '''
        help_template = "value must be of the form '8.5 x 11 in'."
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_paper_dimension_string,
            help_template=help_template,
            )

    def append_pitch_range(
        self,
        spaced_attribute_name,
        ):
        r'''Appends pitch range.

        Returns prompt.
        '''
        help_template = 'value must be pitch range.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        setup_statements.append('evaluated_input = pitchtools.PitchRange({})')
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_pitch_range_or_none,
            help_template=help_template,
            setup_statements=setup_statements,
            )
        self._setup_statements[-1] = setup_statements

    def append_pitch_range_string(
        self,
        spaced_attribute_name,
        ):
        r'''Appends symbolic pitch range string.

        Returns prompt.
        '''
        help_template = 'value must be pitch range string. Ex: [A0, C8].'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=pitchtools.PitchRange.is_range_string,
            help_template=help_template,
            )

    def append_positive_integer(
        self,
        spaced_attribute_name,
        ):
        r'''Appends positive integer.

        Returns prompt.
        '''
        help_template = 'value must be positive integer.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=mathtools.is_positive_integer,
            help_template=help_template,
            )

    def append_positive_integer_power_of_two(
        self,
        spaced_attribute_name,
        ):
        r'''Appends positive integer power of two.

        Returns prompt.
        '''
        help_template = 'value must be positive integer power of two.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=mathtools.is_positive_integer_power_of_two,
            help_template=help_template,
            )

    def append_positive_integer_powers_of_two(
        self,
        spaced_attribute_name,
        ):
        r'''Appends positive integer powers of two.

        Returns prompt.
        '''
        help_template = 'value must be list or tuple of'
        help_template += ' positive integer powers of two.'
        validation_function = mathtools.all_are_positive_integer_powers_of_two
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            )

    def append_positive_integers(
        self,
        spaced_attribute_name,
        ):
        r'''Appends positive integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of positive integers.'
        function = lambda expr: all(
            mathtools.is_positive_integer(x) for x in expr)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            )

    def append_snake_case_file_name(
        self,
        spaced_attribute_name,
        ):
        r'''Appends snake case file name.

        Returns prompt.
        '''
        help_template = 'value must be snake case file name.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=stringtools.is_snake_case_file_name,
            help_template=help_template,
            )

    def append_snake_case_file_name_with_extension(
        self,
        spaced_attribute_name,
        ):
        r'''Appends snake case file name with extension.

        Returns prompt.
        '''
        help_template = 'value must be snake case file name with extension.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=\
                stringtools.is_snake_case_file_name_with_extension,
            help_template=help_template,
            )

    def append_snake_case_package_name(
        self,
        spaced_attribute_name,
        ):
        r'''Appends snake case package name.

        Returns prompt.
        '''
        help_template = 'value must be snake case package name, 3 <= length.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_snake_case_package_name,
            help_template=help_template,
            )

    def append_snake_case_string(
        self,
        spaced_attribute_name,
        allow_empty=False,
        ):
        r'''Appends snake case string.

        Returns prompt.
        '''
        def is_nonempty_snake_case_string(expr):
            if stringtools.is_snake_case(expr):
                return bool(expr)
            return False
        if allow_empty:
            help_template = 'value must be snake case string.'
            validation_function = stringtools.is_snake_case
        else:
            help_template = 'value must be nonempty snake case string.'
            validation_function = is_nonempty_snake_case_string
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            )

    def append_space_delimited_lowercase_string(
        self,
        spaced_attribute_name,
        ):
        r'''Appends space-delimited lowercase string.

        Returns prompt.
        '''
        help_template = 'value must be space-delimited lowercase string.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=stringtools.is_space_delimited_lowercase,
            help_template=help_template,
            )

    def append_string(
        self,
        spaced_attribute_name,
        allow_empty=True,
        ):
        r'''Appends string.

        Returns prompt.
        '''
        if allow_empty:
            validation_function = PromptMakerMixin.is_string
            help_template = 'value must be string.'
        else:
            validation_function = PromptMakerMixin.is_nonempty_string
            help_template = 'value must be nonempty string.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            )

    def append_string_or_none(
        self,
        spaced_attribute_name,
        ):
        r'''Appends string or none.

        Returns prompt.
        '''
        help_template = 'value must be string or none.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_string_or_none,
            help_template=help_template,
            )

    def append_strings(
        self,
        spaced_attribute_name,
        ):
        r'''Appends strings.

        Returns prompt.
        '''
        help_template = 'value must be tuple of strings.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.are_strings,
            help_template=help_template,
            )

    def append_tempo(
        self,
        spaced_attribute_name,
        ):
        r'''Appends tempo.

        Returns prompt.
        '''
        help_template = 'value must successfully initialize tempo.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=PromptMakerMixin.is_tempo_token,
            help_template=help_template,
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
            validation_function=PromptMakerMixin.is_yes_no_string,
            help_template=help_template,
            include_chevron=include_chevron,
            )

    @staticmethod
    def are_articulation_tokens(expr):
        r'''Predicate.
        '''
        if isinstance(expr, (tuple, list)):
            return all(is_articulation_token(x) for x in expr)

    @staticmethod
    def are_duration_tokens(expr):
        r'''Predicate.
        '''
        if isinstance(expr, (tuple, list)):
            return all(is_duration_token(x) for x in expr)

    @staticmethod
    def are_dynamic_tokens(expr):
        r'''Predicate.
        '''
        if isinstance(expr, (tuple, list)):
            return all(is_dynamic_token(x) for x in expr)

    @staticmethod
    def are_hairpin_tokens(expr):
        r'''Predicate.
        '''
        if isinstance(expr, (tuple, list)):
            return all(is_hairpin_token(x) for x in expr)

    @staticmethod
    def are_lists(expr):
        r'''Predicate.
        '''
        if isinstance(expr, (tuple, list)):
            return all(is_list(x) for x in expr)

    @staticmethod
    def are_strings(expr):
        r'''Predicate.
        '''
        if isinstance(expr, (tuple, list)):
            return all(is_string(x) for x in expr)

    @staticmethod
    def is_argument_range_string(expr):
        r'''Predicate.
        '''
        pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
        return pattern.match(expr) is not None

    @staticmethod
    def is_articulation_token(expr):
        r'''Predicate.
        '''
        try:
            result = indicatortools.Articulation(expr)
            return isinstance(result, indicatortools.Articulation)
        except:
            return False

    @staticmethod
    def is_boolean(expr):
        r'''Predicate.
        '''
        return isinstance(expr, bool)

    @staticmethod
    def is_class_name_or_none(expr):
        r'''Predicate.
        '''
        return expr is None or stringtools.is_upper_camel_case(expr)

    @staticmethod
    def is_clef_token(expr):
        r'''Predicate.
        '''
        try:
            result = indicatortools.Clef(expr)
            return isinstance(result, indicatortools.Clef)
        except:
            return False

    @staticmethod
    def is_direction_string(expr):
        r'''Predicate.
        '''
        return expr in ('up', 'down')

    @staticmethod
    def is_duration_token(expr):
        r'''Predicate.
        '''
        try:
            durationtools.Duration(expr)
            return True
        except:
            return False

    @staticmethod
    def is_dynamic_token(expr):
        r'''Predicate.
        '''
        try:
            result = indicatortools.Dynamic(expr)
            return isinstance(result, indicatortools.Dynamic)
        except:
            return False

    @staticmethod
    def is_hairpin_token(expr):
        r'''Predicate.
        '''
        return spannertools.Hairpin._is_hairpin_token(expr)

    @staticmethod
    def is_identifier(expr, allow_spaces=False):
        r'''Predicate.
        '''
        if not isinstance(expr, str):
            return False
        if len(expr) < 1:
            return False
        if expr[0] in '0123456789':
            return False
        for _ in expr:
            if allow_spaces:
                if not (_.isalnum() or _ == '_' or _ == ' '):
                    return False
            else:
                if not (_.isalnum() or _ == '_'):
                    return False
        return True

    @staticmethod
    def is_integer(expr):
        r'''Predicate.
        '''
        return isinstance(expr, int)

    @staticmethod
    def is_integer_in_range(expr, start=None, stop=None, allow_none=False):
        r'''Predicate.
        '''
        if expr is None and allow_none:
            return True
        if PromptMakerMixin.is_integer(expr) and \
            (start is None or start <= expr) and \
            (stop is None or expr <= stop):
            return True
        return False

    @staticmethod
    def is_integer_or_none(expr):
        r'''Predicate.
        '''
        return expr is None or is_integer(expr)

    @staticmethod
    def is_list(expr):
        r'''Predicate.
        '''
        return isinstance(expr, list)

    @staticmethod
    def is_markup(expr):
        r'''Predicate.
        '''
        return isinstance(expr, markuptools.Markup)

    @staticmethod
    def is_markup_token(expr):
        r'''Predicate.
        '''
        try:
            result = markuptools.Markup(expr)
            return isinstance(result, markuptools.Markup)
        except:
            return False

    @staticmethod
    def is_named_pitch(expr):
        r'''Predicate.
        '''
        return isinstance(expr, NamedPitch)

    @staticmethod
    def is_negative_integer(expr):
        r'''Predicate.
        '''
        return is_integer(expr) and expr < 0

    @staticmethod
    def is_nonempty_string(expr):
        r'''Predicate.
        '''
        return isinstance(expr, str) and bool(expr)

    @staticmethod
    def is_nonnegative_integer(expr):
        r'''Predicate.
        '''
        return is_integer(expr) and expr <= 0

    @staticmethod
    def is_nonpositive_integer(expr):
        r'''Predicate.
        '''
        return is_integer(expr) and 0 <= expr

    @staticmethod
    def is_page_layout_unit(expr):
        r'''Predicate.
        '''
        return expr in ('in', 'mm', 'cm', 'pt', 'pica')

    @staticmethod
    def is_paper_dimension_string(expr):
        r'''Predicate.
        '''
        if not isinstance(expr, str):
            return False
        parts = expr.split()
        if not len(parts) == 4:
            return False
        width, x, height, units = parts
        try:
            float(width) 
        except ValueError:
            return False
        try:
            float(height) 
        except ValueError:
            return False
        if not x == 'x':
            return False
        if not is_page_layout_unit(units):
            return False
        return True

    @staticmethod
    def is_pitch_range_or_none(expr):
        r'''Predicate.
        '''
        return isinstance(expr, (pitchtools.PitchRange, type(None)))

    @staticmethod
    def is_positive_integer(expr):
        r'''Predicate.
        '''
        return is_integer(expr) and 0 < expr

    @staticmethod
    def is_string(expr):
        r'''Predicate.
        '''
        return isinstance(expr, str)

    @staticmethod
    def is_string_or_none(expr):
        r'''Predicate.
        '''
        return isinstance(expr, (str, type(None)))

    @staticmethod
    def is_tempo_token(expr):
        r'''Predicate.
        '''
        import abjad
        from ide.tools import idetools
        try:
            namespace = abjad.__dict__.copy()
            command = 'tempo = indicatortools.Tempo({})'.format(expr)
            result = idetools.IOManager().execute_string(
                command,
                attribute_names=('tempo',),
                local_namespace=namespace,
                )
            tempo = result[0]
            return isinstance(tempo, indicatortools.Tempo)
        except:
            return False

    @staticmethod
    def is_snake_case_package_name(expr):
        r'''Predicate.
        '''
        return stringtools.is_snake_case_package_name(expr)

    @staticmethod
    def is_yes_no_string(expr):
        r'''Predicate.
        '''
        return 'yes'.startswith(expr.lower()) or 'no'.startswith(expr.lower())