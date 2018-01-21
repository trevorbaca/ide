import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_illustration_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        directory = ide.Path('red_score', 'materials', 'red_pitch_classes')
        ly = directory('illustration.ly')
        ly.remove()
        pdf = directory('illustration.pdf')
        pdf.remove()
        maker = directory('__make_material_pdf__.py')
        maker.remove()

        abjad_ide('red %rpc pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making red pitch classes PDF ...'in transcript
        assert f'Removing {ly.trim()} ...' not in transcript
        assert f'Removing {pdf.trim()} ...' not in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Writing {ly.trim()} ...' in transcript
        assert f'Writing {pdf.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {pdf.trim()} ...' in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()

        abjad_ide('red %rpc pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making red pitch classes PDF ...'in transcript
        assert f'Removing {ly.trim()} ...' in transcript
        assert f'Removing {pdf.trim()} ...' in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Writing {ly.trim()} ...' in transcript
        assert f'Writing {pdf.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {pdf.trim()} ...' in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()


def test_AbjadIDE_make_illustration_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        directory = ide.Path('red_score', 'segments', 'A')
        ly = directory('illustration.ly')
        ly.remove()
        pdf = directory('illustration.pdf')
        pdf.remove()
        maker = directory('__make_segment_pdf__.py')
        maker.remove()

        abjad_ide('red %A pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making segment A PDF ...'in transcript
        assert f'Removing {ly.trim()} ...' not in transcript
        assert f'Removing {pdf.trim()} ...' not in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Writing {ly.trim()} ...' in transcript
        assert f'Writing {pdf.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {pdf.trim()} ...' in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()

        abjad_ide('red %A pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making segment A PDF ...'in transcript
        assert f'Removing {ly.trim()} ...' in transcript
        assert f'Removing {pdf.trim()} ...' in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Writing {ly.trim()} ...' in transcript
        assert f'Writing {pdf.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {pdf.trim()} ...' in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()
