import abjad


blue_rhythm_1 = abjad.rmakers.TaleaRhythmMaker(
    talea=abjad.rmakers.Talea(
        counts=(2, 2, -3),
        denominator=8,
        ),
    split_divisions_by_counts=(2, 1),
    extra_counts_per_division=(3, 1, 1),
    )
