import abjad
from red_score.materials.magic_numbers.definition import magic_numbers


def make_lilypond_file(magic_numbers):
    strings = [str(_) for _ in magic_numbers]
    string = ' '.join(strings)
    markup = abjad.Markup(string)
    lilypond_file = abjad.LilyPondFile()
    lilypond_file.items.append(markup)
    return lilypond_file

lilypond_file = make_lilypond_file(magic_numbers)
