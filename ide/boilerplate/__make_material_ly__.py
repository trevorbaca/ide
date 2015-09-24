# -*- coding: utf-8 -*-
import os
import sys
import traceback
from abjad.tools.topleveltools import persist


if __name__ == '__main__':
    
    try:
        from __illustrate__ import lilypond_file
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = os.path.dirname(__file__)
        candidate_path = os.path.join(
            current_directory,
            'illustration.candidate.ly',
            )
        persist(lilypond_file).as_ly(candidate_path)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)