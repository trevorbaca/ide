# -*- coding: utf-8 -*-
import os
import sys
import traceback
from abjad import *
from {score_package_name}.materials.{material_package_name}.definition import {material_package_name}


if __name__ == '__main__':

    lilypond_file = lilypondfiletools.make_basic_lilypond_file({material_package_name})

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