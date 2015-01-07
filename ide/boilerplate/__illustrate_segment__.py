# -*- encoding: utf-8 -*-
import os
import sys
import traceback
from abjad import persist


if __name__ == '__main__':
    try:
        from definition import segment_maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        lilypond_file = segment_maker()
    except:
        traceback.print_exc()
        sys.exit(1)

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