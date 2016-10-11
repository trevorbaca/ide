# -*- coding: utf-8 -*-
import abjad


markup_inventory = abjad.markuptools.MarkupInventory(
    [
        abjad.markuptools.Markup(
            contents=(
                abjad.markuptools.MarkupCommand(
                    'bold',
                    ['staccatissimo', 'luminoso']
                    ),
                ),
            ),
        abjad.markuptools.Markup(
            contents=(
                abjad.markuptools.MarkupCommand(
                    'italic',
                    ['serenamente']
                    ),
                ),
            ),
        ]
    )