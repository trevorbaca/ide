# -*- coding: utf-8 -*-
import abjad


tempo_inventory = abjad.indicatortools.TempoInventory(
    [
        abjad.indicatortools.Tempo(
            reference_duration=abjad.durationtools.Duration(1, 8),
            units_per_minute=72,
            ),
        abjad.indicatortools.Tempo(
            reference_duration=abjad.durationtools.Duration(1, 8),
            units_per_minute=108,
            ),
        abjad.indicatortools.Tempo(
            reference_duration=abjad.durationtools.Duration(1, 8),
            units_per_minute=90,
            ),
        abjad.indicatortools.Tempo(
            reference_duration=abjad.durationtools.Duration(1, 8),
            units_per_minute=135,
            ),
        ]
    )