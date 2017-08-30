#! /usr/bin/env python
import abjad
import ide
import pathlib
import sys
import traceback


if __name__ == '__main__':
    with abjad.Timer() as timer:
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
            from red_score.segments.segment_01.__metadata__ import metadata as previous_metadata
        except ImportError:
            traceback.print_exc()
            sys.exit(1)
        try:
            result = segment_maker(
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
            lilypond_file, metadata = result
        except:
            traceback.print_exc()
            sys.exit(1)
        try:
            directory = pathlib.Path(__file__).parent
            directory = ide.PackagePath(directory)
            directory._write_metadata_py(metadata)
        except:
            traceback.print_exc()
            sys.exit(1)
        total_time = int(timer.elapsed_time)
        identifier = abjad.String('second').pluralize(total_time)
        message = f'Abjad runtime {total_time} {identifier} ...'
        print(message)
    try:
        directory = pathlib.Path(__file__).parent
        directory = ide.PackagePath(directory)
        target = directory / 'illustration.pdf'
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_pdf(target)
        total_time = int(timer.elapsed_time)
        identifier = abjad.String('second').pluralize(total_time)
        message = f'LilyPond runtime {total_time} {identifier} ...'
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
