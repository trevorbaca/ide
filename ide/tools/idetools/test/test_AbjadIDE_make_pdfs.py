import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_pdfs_01():

    with ide.Test():
        can_illustrate = ['magic_numbers', 'ranges', 'tempi']
        can_not_illustrate = ['performers', 'time_signatures']
        for name in can_illustrate:
            directory = ide.Path('red_score', 'materials', name)
            target = directory / 'illustration.pdf'
            target.remove()

        abjad_ide('red mm pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            directory = ide.Path('red_score', 'materials', name)
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
            directory = ide.Path('red_score', 'materials', name)
            illustrate = directory / '__illustrate__.py'
            assert f'Can not find {illustrate.trim()} ...' in transcript

        abjad_ide('red mm pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            directory = ide.Path('red_score', 'materials', name)
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

        abjad_ide('red mm **llus q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            path = ide.Path('red_score', 'materials', name, 'illustration.pdf')
            assert "Matching '**llus' to 3 files ..." in transcript

        abjad_ide('red mm **pdf q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            path = ide.Path('red_score', 'materials', name, 'illustration.pdf')
            assert "Matching '**pdf' to 3 files ..." in transcript

        abjad_ide('red mm ** q')
        transcript = abjad_ide.io.transcript
        for name in can_illustrate:
            path = ide.Path('red_score', 'materials', name, 'illustration.pdf')
            assert "Matching '**' to 3 files ..." in transcript

        abjad_ide('red mm **asdf q')
        transcript = abjad_ide.io.transcript
        assert "Matching '**asdf' to no PDFS ..."


def test_AbjadIDE_make_pdfs_02():

    with ide.Test():
        names = ['A', 'B', 'C']
        for name in names:
            target = ide.Path('red_score', 'segments', name)
            target /= 'illustration.pdf'
            target.remove()

        abjad_ide('red gg pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in names:
            directory = ide.Path('red_score', 'segments', name)
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

        abjad_ide('red gg **llus q')
        transcript = abjad_ide.io.transcript
        for name in names:
            path = ide.Path('red_score', 'segments', name, 'illustration.pdf')
            assert "Matching '**llus' to 3 files ..." in transcript

        abjad_ide('red gg **pdf q')
        transcript = abjad_ide.io.transcript
        for name in names:
            path = ide.Path('red_score', 'segments', name, 'illustration.pdf')
            assert "Matching '**pdf' to 3 files ..." in transcript

        abjad_ide('red gg ** q')
        transcript = abjad_ide.io.transcript
        for name in names:
            path = ide.Path('red_score', 'segments', name, 'illustration.pdf')
            assert "Matching '**' to 3 files ..." in transcript

        abjad_ide('red gg **asdf q')
        transcript = abjad_ide.io.transcript
        assert "Matching '**asdf' to 0 files ..." in transcript
