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
            previous_metadata = None
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
            current_directory = pathlib.Path(__file__).parent
            dummy_session = ide.tools.idetools.Session()
            abjad_ide = ide.tools.idetools.AbjadIDE(
                session=dummy_session,
                )
            abjad_ide._write_metadata_py(
                current_directory,
                metadata,
                )
        except:
            traceback.print_exc()
            sys.exit(1)
        #message = 'Abjad runtime {} {} ...'
        #total_time = int(timer.elapsed_time)
        #identifier = abjad.String('second').pluralize(total_time)
        #message = message.format(total_time, identifier)
        #print(message)
    try:
        current_directory = pathlib.Path(__file__).parent
        ly_path = current_directory.joinpath('illustration.ly')
        pdf_path = current_directory.joinpath('illustration.pdf')
        output_paths = (ly_path, pdf_path)
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_pdf(pdf_path)
        #message = 'LilyPond runtime {} {} ...'
        #total_time = int(timer.elapsed_time)
        #identifier = abjad.String('second').pluralize(total_time)
        #message = message.format(total_time, identifier)
        #print(message)
        #for output_path in output_paths:
        #    message = 'writing {} ...'
        #    path = ide.tools.idetools.AbjadIDE._trim_path(output_path)
        #    message = message.format(path)
        #    print(message)
    except:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
