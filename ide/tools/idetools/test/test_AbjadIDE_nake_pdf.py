import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_nake_pdf_02():
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

        abjad_ide('red %A pdfn q')
        transcript = abjad_ide.io.transcript
        assert 'Making segment A PDF ...'in transcript
        assert f'Removing {ly.trim()} ...' not in transcript
        assert f'Removing {pdf.trim()} ...' not in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Writing {ly.trim()} ...' in transcript
        assert f'Writing {pdf.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {pdf.trim()} ...' not in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()
