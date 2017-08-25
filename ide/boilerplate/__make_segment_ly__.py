import abjad
import ide
import pathlib
import sys
import traceback


if __name__ == '__main__':

    try:
        from definition import segment_maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __metadata__ import metadata as metadata
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            result = segment_maker(
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
            lilypond_file, metadata = result
        message = 'Abjad runtime: {{}} sec.'
        message = message.format(int(timer.elapsed_time))
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = pathlib.Path(__file__).parent
        dummy_session = ide.Session()
        abjad_ide = ide.AbjadIDE(
            session=dummy_session,
            )
        abjad_ide._write_metadata_py(
            current_directory,
            metadata,
            )
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        current_directory = pathlib.Path(__file__).parent
        ly_path = current_directory / 'illustration.ly'
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_ly(ly_path)
        message = 'LilyPond runtime: {{}} sec.'
        message = message.format(int(timer.elapsed_time))
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
