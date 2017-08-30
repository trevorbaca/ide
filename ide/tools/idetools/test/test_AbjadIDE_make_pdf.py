import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.
    '''

    source = ide.PackagePath('red_score').materials / 'magic_numbers'
    source /= 'illustration.ly'
    with ide.Test(keep=[source]):
        illustrate = source.with_name('__illustrate__.py')
        target = source.with_suffix('.pdf')
        source.remove()
        target.remove()

        input_ = 'red~score %magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' not in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)

        input_ = 'red~score %magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)


def test_AbjadIDE_make_pdf_02():
    r'''In segment directory.
    '''

    source = ide.PackagePath('red_score').segments / 'segment_01'
    source /= 'illustration.ly'
    with ide.Test(keep=[source]):
        illustrate = source.with_name('__illustrate__.py')
        target = source.with_suffix('.pdf')
        source.remove()
        target.remove()

        input_ = 'red~score %A pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' not in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)

        input_ = 'red~score %A pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making PDF ...'in transcript
        assert f'Removing {source.trim()} ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)
