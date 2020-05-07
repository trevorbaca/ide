import abjad

blue_rhythm_1 = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(counts=(2, 2, -3), denominator=8),
    split_divisions_by_counts=(2, 1),
    extra_counts_per_division=(3, 1, 1),
)
