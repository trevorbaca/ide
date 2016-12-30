# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


# TODO: make (pdfm) work in this material package
#def test_AbjadIDE_trash_pdf_01():
#    r'''In material directory.
#    '''
#
#    material_directory = os.path.join(
#        configuration.abjad_ide_example_scores_directory,
#        'red_example_score',
#        'red_example_score',
#        'materials',
#        'magic_numbers',
#        )
#    pdf_path = os.path.join(material_directory, 'illustration.pdf')
#
#    input_ = 'red~example~score mm magic~numbers pdfm q'
#    abjad_ide._start(input_=input_)
#    assert os.path.isfile(pdf_path)
#    input_ = 'red~example~score mm magic~numbers pdft q'
#    abjad_ide._start(input_=input_)
#    assert not os.path.exists(pdf_path)


def test_AbjadIDE_trash_pdf_02():
    r'''In segment directory.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')

    with abjad.systemtools.FilesystemState(keep=[ly_path]):
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(pdf_path)
        input_ = 'red~example~score gg A pdft q'
        abjad_ide._start(input_=input_)
        assert not os.path.exists(pdf_path)
