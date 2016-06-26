# -*- coding: utf-8 -*-
import abjad
from red_example_score.materials.magic_numbers.definition import magic_numbers


def make_lilypond_file(magic_numbers):
    strings = [str(_) for _ in magic_numbers]
    string = ' '.join(strings)
    markup = abjad.markuptools.Markup(string)
    lilypond_file = abjad.lilypondfiletools.LilyPondFile()
    lilypond_file.items.append(markup)
    return lilypond_file

lilypond_file = make_lilypond_file(magic_numbers)