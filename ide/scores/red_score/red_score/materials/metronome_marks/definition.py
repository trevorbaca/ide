import abjad


metronome_marks = abjad.OrderedDict(
    [
        (
            72,
            abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 8), units_per_minute=72
            ),
        ),
        (
            108,
            abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 8), units_per_minute=108
            ),
        ),
        (
            90,
            abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 8), units_per_minute=90
            ),
        ),
        (
            135,
            abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 8), units_per_minute=135
            ),
        ),
    ]
)
