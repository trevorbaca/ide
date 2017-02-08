# -*- coding: utf-8 -*-
import abjad


class SargassoMeasureMaker(abjad.abctools.AbjadObject):
    r'''Sargasso measure maker.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_measure_denominator',
        '_measure_numerator_talea',
        '_measure_division_denominator',
        '_measure_division_talea',
        '_total_duration',
        '_measures_are_scaled',
        '_measures_are_split',
        '_measures_are_shuffled',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        measure_denominator=None,
        measure_numerator_talea=None,
        measure_division_denominator=None,
        measure_division_talea=None,
        total_duration=None,
        measures_are_scaled=False,
        measures_are_split=False,
        measures_are_shuffled=False,
        ):
        self._measure_denominator = measure_denominator
        self._measure_numerator_talea = measure_numerator_talea
        self._measure_division_denominator = measure_division_denominator
        self._measure_division_talea = measure_division_talea
        self._total_duration = total_duration
        self._measures_are_scaled = measures_are_scaled
        self._measures_are_split = measures_are_split
        self._measures_are_shuffled = measures_are_shuffled

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls sargasso measure maker.

        Returns list of measures.
        '''
        measure_denominator = self.measure_denominator
        measure_numerator_talea = self.measure_numerator_talea
        measure_division_denominator = self.measure_division_denominator
        measure_division_talea = self.measure_division_talea
        total_duration = self.total_duration
        measures_are_scaled = self.measures_are_scaled
        measures_are_split = self.measures_are_split
        measures_are_shuffled = self.measures_are_shuffled

        #print measure_denominator
        #print measure_numerator_talea
        #print measure_division_denominator
        #print measure_division_talea
        #print total_duration
        #print measures_are_scaled
        #print measures_are_split
        #print measures_are_shuffled

        assert abjad.mathtools.is_nonnegative_integer_power_of_two(
            measure_denominator)
        assert abjad.mathtools.is_nonnegative_integer_power_of_two(
            measure_division_denominator)
        assert measure_denominator <= measure_division_denominator

        assert all(abjad.mathtools.is_positive_integer(x)
            for x in measure_numerator_talea)
        assert all(abjad.mathtools.is_positive_integer(x)
            for x in measure_division_talea)
        total_duration = abjad.Duration(total_duration)

        weight = int(measure_denominator * total_duration)
        measure_numerators = abjad.sequencetools.repeat_sequence_to_weight(
            measure_numerator_talea, weight)
        #print measure_numerators

        weight = int(measure_division_denominator * total_duration)
        measure_divisions = abjad.sequencetools.repeat_sequence_to_weight(
            measure_division_talea, weight)
        #print measure_divisions

        multiplier = measure_division_denominator / measure_denominator
        multiplied_measure_numerators = [
            multiplier * x for x in measure_numerators]
        #print multiplied_measure_numerators

        measure_divisions_by_measure = abjad.sequencetools.split_sequence(
            measure_divisions,
            multiplied_measure_numerators,
            cyclic=True,
            overhang=True,
            )
        #print measure_divisions_by_measure

        meter_multipliers = [
            abjad.Multiplier(1)
            for x in measure_divisions_by_measure
            ]

        if measures_are_scaled:

            meter_multipliers = []
            for measure_index, multiplied_measure_numerator in \
                enumerate(multiplied_measure_numerators):
                possible_multipliers = self._get_possible_meter_multipliers(
                    multiplied_measure_numerator)
                meter_multiplier = self._select_meter_multiplier(
                    possible_multipliers, measure_index)
                meter_multipliers.append(meter_multiplier)
            #print meter_multipliers

            prolated_measure_numerators = []
            for meter_multiplier, multiplied_measure_numerator in \
                zip(meter_multipliers, multiplied_measure_numerators):
                prolated_measure_numerator = \
                    multiplied_measure_numerator / meter_multiplier
                assert abjad.mathtools.is_integer_equivalent_number(
                    prolated_measure_numerator)
                prolated_measure_numerator = int(prolated_measure_numerator)
                prolated_measure_numerators.append(prolated_measure_numerator)
            #print prolated_measure_numerators

            measure_divisions = \
                abjad.sequencetools.repeat_sequence_to_weight(
                measure_division_talea, sum(prolated_measure_numerators))
            #print measure_divisions

            measure_divisions_by_measure = \
                abjad.sequencetools.split_sequence(
                measure_divisions,
                prolated_measure_numerators,
                cyclic=True,
                overhang=True)
            #print measure_divisions_by_measure

        measure_tokens = zip(meter_multipliers, measure_divisions_by_measure)
        #for x in measure_tokens: print x

        if measures_are_split:
            ratio = [1, 1]
        else:
            ratio = [1]

        divided_measure_tokens = []
        for meter_multiplier, measure_divisions in measure_tokens:
            division_lists = \
                abjad.sequencetools.partition_sequence_by_ratio_of_lengths(
                    measure_divisions, ratio)
            for division_list in division_lists:
                if division_list:
                    token = (meter_multiplier, division_list)
                    divided_measure_tokens.append(token)
        #for x in divided_measure_tokens: print x

        if measures_are_shuffled:
            divided_measure_tokens = self._permute_divided_measure_tokens(
                divided_measure_tokens)

        meter_tokens = []
        for meter_multiplier, measure_divisions in divided_measure_tokens:
            measure_duration = meter_multiplier * abjad.Multiplier(
                sum(measure_divisions), measure_division_denominator)
            meter_base_unit = meter_multiplier * abjad.Multiplier(
                min(measure_divisions), measure_division_denominator)
            meter_denominator = meter_base_unit.denominator
            meter_token = \
                abjad.mathtools.NonreducedFraction(
                    measure_duration).with_multiple_of_denominator(
                meter_denominator)
            meter_tokens.append(meter_token)
        #print meter_tokens

        division_tokens = []
        for measure_duration, division_token in divided_measure_tokens:
            division_tokens.append(division_token)
        #print division_tokens

        measures = []
        for meter_token, division_token in zip(meter_tokens, division_tokens):
            leaves = abjad.scoretools.make_leaves_from_talea(
                division_token, measure_division_denominator)
            measure = abjad.Measure(
                meter_token,
                leaves,
                implicit_scaling=True,
                )
            measures.append(measure)
        #print measures

        selection = abjad.select(measures)

        #return measures
        return selection

    def __eq__(self, argument):
        r'''Is true when `argument` is a sargasso measure-maker with type and 
        public properties equal to those of this sargasso measure-maker.
        Otherwise false.

        Returns true or false.
        '''
        return abjad.StorageFormatManager.compare(self, argument)

    def __hash__(self):
        r'''Hashes sargasso measure-maker.
        '''
        hash_values = abjad.StorageFormatManager.get_hash_values(
            self)
        return hash(hash_values)

    def __illustrate__(self, **keywords):
        r'''Illustrates sargasso measure maker.

        Returns LilyPond file.
        '''
        measures = self()
        staff = abjad.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        score = abjad.Score([staff])
        illustration = abjad.lilypondfiletools.make_basic_lilypond_file(score)
        measures = score._get_components(abjad.Measure)
        for measure in measures:
            beam = abjad.Beam()
            abjad.attach(beam, [measure])
        score.add_final_bar_line()
        return illustration

    ### PRIVATE PROPERTIES ###

    @property
    def _input_demo_values(self):
        return [
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea',
                [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', abjad.Duration(44, 8)),
            ('measures_are_scaled', True),
            ('measures_are_split', True),
            ('measures_are_shuffled', True),
        ]

    ### PRIVATE METHODS ###

    def _get_possible_meter_multipliers(self, multiplied_measure_numerator):
        possible_meter_multipliers = []
        assert int(multiplied_measure_numerator) == \
            multiplied_measure_numerator
        multiplied_measure_numerator = int(multiplied_measure_numerator)
        stop_value = 2 * multiplied_measure_numerator
        for denominator in range(multiplied_measure_numerator, stop_value):
            pair = (multiplied_measure_numerator, denominator)
            possible_meter_multiplier = abjad.Multiplier(pair)
            possible_meter_multipliers.append(possible_meter_multiplier)
        return possible_meter_multipliers

    @staticmethod
    def _make_measure_string(measure):
        time_signature = measure.time_signature
        pair = (time_signature.numerator, time_signature.denominator)
        contents_string = ' '.join([str(x) for x in measure])
        result = '{}({}, {!r}, implicit_scaling={})'
        result = result.format(
            type(measure).__name__,
            pair,
            contents_string,
            measure.implicit_scaling,
            )
        return result

    def _make_output_material_lines(self, output_material):
        lines = []
        lines.append('{} = ['.format(self._package_name))
        for measure in output_material[:-1]:
            line = self._make_measure_string(measure)
            line = 'abjad.scoretools.' + line
            lines.append('\t{},'.format(line))
        line = output_material[-1]._one_line_input_string
        lines.append('\tabjad.scoretools.{}]'.format(line))
        lines = [line + '\n' for line in lines]
        return lines

    def _permute_divided_measure_tokens(self, divided_measure_tokens):
        modulus_of_permutation = 5
        len_divided_measure_tokens = len(divided_measure_tokens)
        assert abjad.mathtools.are_relatively_prime(
            [modulus_of_permutation, len_divided_measure_tokens])
        permutation = [(5 * x) % len_divided_measure_tokens
            for x in range(len_divided_measure_tokens)]
        divided_measure_tokens = abjad.sequencetools.permute_sequence(
                divided_measure_tokens, permutation)
        return divided_measure_tokens

    def _select_meter_multiplier(
        self, 
        possible_meter_multipliers, 
        measure_index,
        ):
        possible_meter_multipliers = \
            abjad.datastructuretools.CyclicTuple(possible_meter_multipliers)
        meter_multiplier = possible_meter_multipliers[5 * measure_index]
        return meter_multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def measure_denominator(self):
        r'''Gets measure denominator of sargasso measure maker.

        Returns positive integer.
        '''
        return self._measure_denominator

    @property
    def measure_division_denominator(self):
        r'''Gets mesaure division denominator of sargasso measure maker.

        Returns positive integer.
        '''
        return self._measure_division_denominator

    @property
    def measure_division_talea(self):
        r'''Gets measure division talea of sargasso measure maker.

        Returns tuple.
        '''
        return self._measure_division_talea

    @property
    def measure_numerator_talea(self):
        r'''Gets measure numerator talea of sargasso measure maker.

        Returns tuple.
        '''
        return self._measure_numerator_talea

    @property
    def measures_are_scaled(self):
        r'''Is true when measures are scaled. Otherwise false.

        Returns true or false.
        '''
        return self._measures_are_scaled

    @property
    def measures_are_shuffled(self):
        r'''Is true when measures are shuffled. Otherwise false.

        Returns true or false.
        '''
        return self._measures_are_shuffled

    @property
    def measures_are_split(self):
        r'''Is true when measures are split. Otherwise false.

        Returns true or false.
        '''
        return self._measures_are_split

    @property
    def total_duration(self):
        r'''Gets total duration of sargasso measure maker.

        Returns duration.
        '''
        return self._total_duration
