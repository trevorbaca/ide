import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'magic_numbers'
        source /= 'illustration.ly'
        illustrate = source.with_name('__illustrate__.py')
        target = source.with_suffix('.pdf')
        source.remove()
        target.remove()

        abjad_ide('red~score %magic pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' not in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()

        abjad_ide('red~score %magic pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()


def test_AbjadIDE_make_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_01'
        source /= 'illustration.ly'
        illustrate = source.with_name('__illustrate__.py')
        target = source.with_suffix('.pdf')
        source.remove()
        target.remove()

        abjad_ide('red~score %A pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' not in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()

        abjad_ide('red~score %A pdfm q')
        transcript = abjad_ide.io.transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()
