import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_collect_lys_01():
    r'''In builds directory.
    '''

    ly_paths = []
    for name in ('_', 'A', 'B'):
        ly_name = f'segment-{name}.ly'
        ly_path = ide.Path('red_score')._segments(ly_name)
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red bb lyc* q')
        transcript = abjad_ide.io.transcript
        for ly_path in ly_paths:
            assert ly_path.is_file()
            assert f'Writing {ly_path.trim()} ...' in transcript
            message = f'No segment breaks found in {ly_path.trim()} ...'
            assert message in transcript
            message = f'No empty bars found in {ly_path.trim()} ...'
            assert message in transcript


def test_AbjadIDE_collect_lys_02():
    r'''In builds _segments directory.
    '''

    ly_paths = []
    for name in ('_', 'A', 'B'):
        ly_name = f'segment-{name}.ly'
        ly_path = ide.Path('red_score')._segments(ly_name)
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red nn lyc* q')
        transcript = abjad_ide.io.transcript
        for ly_path in ly_paths:
            assert ly_path.is_file()
            assert f'Writing {ly_path.trim()} ...' in transcript
