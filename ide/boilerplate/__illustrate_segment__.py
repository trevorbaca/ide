# -*- encoding: utf-8 -*-
import os
import sys
import traceback
from abjad import persist
from ide import idetools


if __name__ == '__main__':

    try:
        from definition import segment_maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __metadata__ import metadata
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        lilypond_file, sticky_settings = segment_maker(metadata=metadata)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        metadata.update(sticky_settings)
        current_directory = os.path.dirname(__file__)
        metadata_py_path = os.path.join(
            current_directory,
            '__metadata__.py',
            )
        controller = idetools.AssetController()
        controller._write_metadata_py(
            metadata, 
            metadata_py_path=metadata_py_path,
            )
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