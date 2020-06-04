import abjad
from abjadext import rmakers

# instruments

instruments = abjad.OrderedDict([("piano", abjad.Piano())])

# metronome marks

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

# pitch ranges

ranges = abjad.OrderedDict(
    [
        ("low", abjad.PitchRange("[A0, C4)")),
        ("high", abjad.PitchRange("[C4, C8]")),
    ]
)

# pitch-classes

red_pitch_classes = abjad.PitchClassSegment([6, 11, 7, 1, 3, 4])

# time signatures

numerators = [_.number for _ in red_pitch_classes]
numerators = [_ % 11 + 1 for _ in numerators]
pairs = [(_, 8) for _ in numerators]
time_signatures = [abjad.TimeSignature(_) for _ in pairs]


class RhythmMaker(rmakers.RhythmMaker):
    """
    Rhythm-maker.

    Dummy class used for testing.
    """

    ### INITIALIZER ###

    def __init__(self):
        pass


def adjust_spacing_sections():
    """
    Example function to test allowing for function files in tools directory.
    """

    pass
