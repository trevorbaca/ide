# -*- coding: utf-8 -*-
import abjad
import os
import sys
import traceback


if __name__ == '__main__':
    
    try:
        with abjad.systemtools.Timer() as timer:
            from __illustrate__ import lilypond_file
        message = 'Abjad runtime {} {} ...'
        total_time = int(timer.elapsed_time)
        identifier = abjad.stringtools.pluralize('second', total_time)
        message = message.format(total_time, identifier)
        print(message)
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = os.path.dirname(__file__)
        candidate_path = os.path.join(
            current_directory,
            'illustration.candidate.pdf',
            )
        with abjad.systemtools.Timer() as timer:
            abjad.persist(lilypond_file).as_pdf(candidate_path)
        message = 'LilyPond runtime {} {} ...'
        total_time = int(timer.elapsed_time)
        identifier = abjad.stringtools.pluralize('second', total_time)
        message = message.format(total_time, identifier)
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)