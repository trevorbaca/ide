import abjad
import definition


def make_lilypond_file(red_pitch_classes):
    strings = [str(_) for _ in red_pitch_classes]
    string = " ".join(strings)
    markup = abjad.Markup(string)
    lilypond_file = abjad.LilyPondFile()
    lilypond_file.items.append(markup)
    return lilypond_file


lilypond_file = make_lilypond_file(definition.red_pitch_classes)
