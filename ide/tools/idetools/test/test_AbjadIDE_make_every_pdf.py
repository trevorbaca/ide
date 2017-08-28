import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_every_pdf_01():

    with ide.Test():
        can_illustrate = ['magic_numbers', 'ranges', 'tempi']
        can_not_illustrate = ['performers', 'time_signatures']
        for name in can_illustrate:
            directory = ide.Path('red_score').materials / name
            target = directory / 'illustration.pdf'
            target.remove()

        input_ = 'red~score mm pdfm* q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        for name in can_illustrate:
            directory = ide.Path('red_score').materials / name
            illustrate = directory / '__illustrate__.py'
            source = directory / 'illustration.ly'
            target = directory / 'illustration.pdf'
            assert 'Making PDF ...' in transcript
            assert f'Removing {abjad_ide._trim(source)} ...' in transcript
            assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
            assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in \
                transcript
            assert f'Opening {abjad_ide._trim(target)} ...' not in transcript
            assert illustrate.is_file()
            assert source.is_file()
            assert target.is_file()
        for name in can_not_illustrate:
            directory = ide.Path('red_score').materials / name
            illustrate = directory / '__illustrate__.py'
            assert f'Can not find {abjad_ide._trim(illustrate)} ...' in \
                transcript

        input_ = 'red~score mm pdfm* q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        for name in can_illustrate:
            directory = ide.Path('red_score').materials / name
            illustrate = directory / '__illustrate__.py'
            source = directory / 'illustration.ly'
            target = directory / 'illustration.pdf'
            assert 'Making PDF ...' in transcript
            assert f'Removing {abjad_ide._trim(source)} ...' in transcript
            assert f'Removing {abjad_ide._trim(target)} ...' in transcript
            assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in \
                transcript
            assert f'Opening {abjad_ide._trim(target)} ...' not in transcript
            assert illustrate.is_file()
            assert source.is_file()
            assert target.is_file()
        for name in can_not_illustrate:
            directory = ide.Path('red_score').materials / name
            illustrate = directory / '__illustrate__.py'
            assert f'Can not find {abjad_ide._trim(illustrate)} ...' in \
                transcript


def test_AbjadIDE_make_every_pdf_02():

    with ide.Test():
        names = ['segment_01', 'segment_02', 'segment_03']
        for name in names:
            directory = ide.Path('red_score').segments
            target = directory / name / 'illustration.pdf'
            target.remove()

        input_ = 'red~score gg pdfm* q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        for name in names:
            directory = ide.Path('red_score').segments / name
            illustrate = directory / '__illustrate__.py'
            source = directory / 'illustration.ly'
            target = directory / 'illustration.pdf'
            assert 'Making PDF ...' in transcript
            assert f'Removing {abjad_ide._trim(source)} ...' in transcript
            assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
            assert f'Removing {abjad_ide._trim(illustrate)} ...' in transcript
            assert f'Writing {abjad_ide._trim(illustrate)} ...' in transcript
            assert f'Interpreting {abjad_ide._trim(illustrate)} ...' in \
                transcript
            assert f'Opening {abjad_ide._trim(target)} ...' not in transcript
            assert illustrate.is_file()
            assert source.is_file()
            assert target.is_file()
