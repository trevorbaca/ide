# -*- encoding: utf-8 -*-
import os
import sys
import traceback
from abjad import persist
from ide.tools import idetools


if __name__ == '__main__':

    try:
        from definition import segment_maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __metadata__ import metadata as segment_metadata
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        PREVIOUS_SEGMENT_METADATA_IMPORT_STATEMENT
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        result = segment_maker(
            segment_metadata=segment_metadata,
            previous_segment_metadata=previous_segment_metadata,
            )
        lilypond_file, segment_metadata = result
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = os.path.dirname(__file__)
        metadata_py_path = os.path.join(
            current_directory,
            '__metadata__.py',
            )
        dummy_session = idetools.Session()
        dummy_io_manager = idetools.IOManager(session=dummy_session)
        controller = idetools.Controller(
            session=dummy_session, 
            io_manager=dummy_io_manager,
            )
        controller._write_metadata_py(
            metadata_py_path,
            segment_metadata, 
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