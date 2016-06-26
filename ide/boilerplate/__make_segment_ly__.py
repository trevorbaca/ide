# -*- coding: utf-8 -*-
import abjad
import ide
import os
import sys
import traceback


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
        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.systemtools.Timer() as timer:
            result = segment_maker(
                segment_metadata=segment_metadata,
                previous_segment_metadata=previous_segment_metadata,
                )
            lilypond_file, segment_metadata = result
        message = 'Abjad runtime: {{}} sec.'
        message = message.format(int(timer.elapsed_time))
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = os.path.dirname(__file__)
        dummy_session = ide.tools.idetools.Session()
        abjad_ide = ide.tools.idetools.AbjadIDE(
            session=dummy_session, 
            )
        abjad_ide._write_metadata_py(
            current_directory,
            segment_metadata, 
            )
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = os.path.dirname(__file__)
        candidate_path = os.path.join(
            current_directory,
            'illustration.candidate.ly',
            )
        with abjad.systemtools.Timer() as timer:
            abjad.persist(lilypond_file).as_ly(candidate_path)
        message = 'LilyPond runtime: {{}} sec.'
        message = message.format(int(timer.elapsed_time))
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)