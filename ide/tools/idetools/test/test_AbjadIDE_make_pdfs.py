import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_pdfs_01():
    r'''In materials directory.
    '''

    with ide.Test():
        directory = ide.Path('red_score').materials
        whitelist = ['metronome_marks', 'red_pitch_classes']
        blacklist = ['instruments', 'ranges', 'time_signatures']
        for name in whitelist:
            ly = directory(name, 'illustration.ly')
            ly.remove()
            pdf = directory(name, 'illustration.pdf')
            pdf.remove()

        abjad_ide('red mm pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in whitelist:
            ly = directory(name, 'illustration.ly')
            pdf = directory(name, 'illustration.pdf')
            maker = directory(name, '__make_pdf__.py')
            assert f"Making {name.replace('_', ' ')} PDF ..." in transcript
            assert f'Removing {ly.trim()} ...' not in transcript
            assert f'Removing {pdf.trim()} ...' not in transcript
            assert f'Writing {maker.trim()} ...' in transcript
            assert f'Interpreting {maker.trim()} ...' in transcript
            assert f'Writing {ly.trim()} ...' in transcript
            assert f'Writing {pdf.trim()} ...' in transcript
            assert f'Removing {maker.trim()} ...' in transcript
            assert f'Opening' not in transcript
            assert ly.is_file()
            assert pdf.is_file()
            assert not maker.exists()
        for name in blacklist:
            ly = directory(name, 'illustration.ly')
            pdf = directory(name, 'illustration.pdf')
            maker = directory(name, '__make_pdf__.py')
            assert f"Making {name.replace('_', ' ')} PDF ..." in transcript
            assert f'Writing {maker.trim()} ...' in transcript
            assert f'Interpreting {maker.trim()} ...' in transcript
            assert f'Removing {maker.trim()} ...' in transcript
            assert not ly.exists()
            assert not pdf.exists()
            assert not maker.exists()

        abjad_ide('red mm **llus q')
        transcript = abjad_ide.io.transcript
        for name in whitelist:
            assert "Matching '**llus' to 2 files ..." in transcript

        abjad_ide('red mm **pdf q')
        transcript = abjad_ide.io.transcript
        for name in whitelist:
            assert "Matching '**pdf' to 2 files ..." in transcript

        abjad_ide('red mm ** q')
        transcript = abjad_ide.io.transcript
        for name in whitelist:
            assert "Matching '**' to 2 files ..." in transcript

        abjad_ide('red mm **asdf q')
        transcript = abjad_ide.io.transcript
        assert "Matching '**asdf' to no PDFS ..."


def test_AbjadIDE_make_pdfs_02():
    r'''In segments directory.
    '''

    with ide.Test():
        directory = ide.Path('red_score').segments
        names = ['_', 'A', 'B']
        for name in names:
            ly = directory('illustration.ly')
            ly.remove()
            pdf = directory('illustration.pdf')
            pdf.remove()
            maker = directory('__make_pdf__.py')
            maker.remove()

        abjad_ide('red gg pdfm* q')
        transcript = abjad_ide.io.transcript
        for name in names:
            ly = directory(name, 'illustration.ly')
            pdf = directory(name, 'illustration.pdf')
            maker = directory(name, '__make_pdf__.py')
            assert f'Making segment {name} PDF ...' in transcript
            assert f'Writing {maker.trim()} ...' in transcript
            assert f'Interpreting {maker.trim()} ...' in transcript
            assert f'Writing {ly.trim()} ...' in transcript
            assert f'Writing {pdf.trim()} ...' in transcript
            assert f'Removing {maker.trim()} ...' in transcript
            assert f'Opening' not in transcript
            assert ly.is_file()
            assert pdf.is_file()
            assert not maker.exists()

        abjad_ide('red gg **llus q')
        transcript = abjad_ide.io.transcript
        for name in names:
            assert "Matching '**llus' to 3 files ..." in transcript

        abjad_ide('red gg **pdf q')
        transcript = abjad_ide.io.transcript
        for name in names:
            assert "Matching '**pdf' to 3 files ..." in transcript

        abjad_ide('red gg ** q')
        transcript = abjad_ide.io.transcript
        for name in names:
            assert "Matching '**' to 3 files ..." in transcript

        abjad_ide('red gg **asdf q')
        transcript = abjad_ide.io.transcript
        assert "Matching '**asdf' to 0 files ..." in transcript
