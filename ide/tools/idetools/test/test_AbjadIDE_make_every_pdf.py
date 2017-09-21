import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_every_pdf_01():

    with ide.Test():
        can_illustrate = ['magic_numbers', 'ranges', 'tempi']
        can_not_illustrate = ['performers', 'time_signatures']
        for name in can_illustrate:
            directory = ide.Path('red_score').materials(name)
            target = directory / 'illustration.pdf'
            target.remove()

        abjad_ide('red~score mm pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            directory = ide.Path('red_score').materials(name)
            illustrate = directory / '__illustrate__.py'
            source = directory / 'illustration.ly'
            target = directory / 'illustration.pdf'
            assert 'Making PDF ...' in transcript
            assert f'Removing {source.trim()} ...' in transcript
            assert f'Removing {target.trim()} ...' not in transcript
            assert f'Interpreting {illustrate.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
            assert illustrate.is_file()
            assert source.is_file()
            assert target.is_file()
        for name in can_not_illustrate:
            directory = ide.Path('red_score').materials(name)
            illustrate = directory / '__illustrate__.py'
            assert f'Can not find {illustrate.trim()} ...' in transcript

        abjad_ide('red~score mm pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            directory = ide.Path('red_score').materials(name)
            illustrate = directory / '__illustrate__.py'
            source = directory / 'illustration.ly'
            target = directory / 'illustration.pdf'
            assert 'Making PDF ...' in transcript
            assert f'Removing {source.trim()} ...' in transcript
            assert f'Removing {target.trim()} ...' in transcript
            assert f'Interpreting {illustrate.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
            assert illustrate.is_file()
            assert source.is_file()
            assert target.is_file()
        for name in can_not_illustrate:
            directory = ide.Path('red_score').materials(name)
            illustrate = directory / '__illustrate__.py'
            assert f'Can not find {illustrate.trim()} ...' in transcript

        abjad_ide('red~score mm **llus q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            path = ide.Path('red_score').material(name, 'illustration.pdf')
            assert f'Opening {path.trim()} ...' in transcript

        abjad_ide('red~score mm **pdf q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            path = ide.Path('red_score').material(name, 'illustration.pdf')
            assert f'Opening {path.trim()} ...' in transcript

        abjad_ide('red~score mm ** q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            path = ide.Path('red_score').material(name, 'illustration.pdf')
            assert f'Opening {path.trim()} ...' in transcript

        abjad_ide('red~score mm **asdf q')
        transcript = abjad_ide.io.transcript
        assert "No PDF '**asdf' ..." in transcript


def test_AbjadIDE_make_every_pdf_02():

    with ide.Test():
        names = ['segment_01', 'segment_02', 'segment_03']
        for name in names:
            directory = ide.Path('red_score').segments()
            target = directory / name / 'illustration.pdf'
            target.remove()

        abjad_ide('red~score gg pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in names:
            directory = ide.Path('red_score').segments(name)
            illustrate = directory / '__illustrate__.py'
            source = directory / 'illustration.ly'
            target = directory / 'illustration.pdf'
            assert 'Making PDF ...' in transcript
            assert f'Removing {source.trim()} ...' in transcript
            assert f'Removing {target.trim()} ...' not in transcript
            assert f'Removing {illustrate.trim()} ...' in transcript
            assert f'Writing {illustrate.trim()} ...' in transcript
            assert f'Interpreting {illustrate.trim()} ...' in transcript
            assert f'Opening {target.trim()} ...' not in transcript
            assert illustrate.is_file()
            assert source.is_file()
            assert target.is_file()

        abjad_ide('red~score gg **llus q')
        transcript = abjad_ide.io.transcript
        for name in names:
            path = ide.Path('red_score').segment(name, 'illustration.pdf')
            assert f'Opening {path.trim()} ...' in transcript

        abjad_ide('red~score gg **pdf q')
        transcript = abjad_ide.io.transcript
        for name in names:
            path = ide.Path('red_score').segment(name, 'illustration.pdf')
            assert f'Opening {path.trim()} ...' in transcript

        abjad_ide('red~score gg ** q')
        transcript = abjad_ide.io.transcript
        for name in names:
            path = ide.Path('red_score').segment(name, 'illustration.pdf')
            assert f'Opening {path.trim()} ...' in transcript

        abjad_ide('red~score gg **asdf q')
        transcript = abjad_ide.io.transcript
        assert "No PDF '**asdf' ..." in transcript
