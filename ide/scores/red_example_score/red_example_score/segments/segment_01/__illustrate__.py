#! /usr/bin/env python
# -*- coding: utf-8 -*-
import abjad
import ide
import os
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
            from __metadata__ import metadata as segment_metadata
        except ImportError:
            traceback.print_exc()
            sys.exit(1)
        try:
            previous_segment_metadata = None
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
        #message = 'Abjad runtime {} {} ...'
        #total_time = int(timer.elapsed_time)
        #identifier = abjad.String('second').pluralize(total_time)
        #message = message.format(total_time, identifier)
        #print(message)
    try:
        current_directory = os.path.dirname(__file__)
        ly_path = os.path.join(
            current_directory,
            'illustration.ly',
            )
        pdf_path = os.path.join(
            current_directory,
            'illustration.pdf',
            )
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
