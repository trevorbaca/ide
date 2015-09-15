# -*- coding: utf-8 -*-
import os
import sys
import traceback
from abjad import *
from red_example_score.materials.magic_numbers.definition import magic_numbers


def make_lilypond_file(magic_numbers):
    strings = [str(_) for _ in magic_numbers]
    string = ' '.join(strings)
    markup = Markup(string)
    lilypond_file = lilypondfiletools.LilyPondFile()
    lilypond_file.items.append(markup)
    return lilypond_file

if __name__ == '__main__':
    lilypond_file = make_lilypond_file(magic_numbers)
    try:
        current_directory = os.path.dirname(__file__)
        candidate_path = os.path.join(
            current_directory,
            'illustration.candidate.pdf',
            )
        persist(lilypond_file).as_pdf(candidate_path)
    except:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)