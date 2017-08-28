import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.
    '''

    source = ide.Path('red_score').materials / 'magic_numbers'
    source /= 'illustration.ly'
    with ide.Test(keep=[source]):
        illustrate = source.with_name('__illustrate__.py')
        target = source.with_suffix('.pdf')
        source.remove()
        target.remove()

        input_ = 'red~score %magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Making PDF ...'in transcript
        assert f'Removing {abjad_ide._trim(source)} ...' not in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)

        input_ = 'red~score %magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Making PDF ...'in transcript
        assert f'Removing {abjad_ide._trim(source)} ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)


def test_AbjadIDE_make_pdf_02():
    r'''In segment directory.
    '''

    source = ide.Path('red_score').segments / 'segment_01'
    source /= 'illustration.ly'
    with ide.Test(keep=[source]):
        illustrate = source.with_name('__illustrate__.py')
        target = source.with_suffix('.pdf')
        source.remove()
        target.remove()

        input_ = 'red~score %A pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Making PDF ...'in transcript
        assert f'Removing {abjad_ide._trim(source)} ...' not in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Removing {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Writing {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)

        input_ = 'red~score %A pdfm q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Making PDF ...'in transcript
        assert f'Removing {abjad_ide._trim(source)} ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Removing {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Writing {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert source.is_file()
        assert target.is_file()
        assert abjad.TestManager._compare_backup(source)
