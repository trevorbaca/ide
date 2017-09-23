import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_collect_segment_lys_01():

    ly_paths = []
    for name in ('A', 'B', 'C'):
        ly_name = f'{name}.ly'
        ly_path = ide.Path('red_score')._segments(ly_name)
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red bb lyc q')
        transcript = abjad_ide.io.transcript
        for ly_path in ly_paths:
            assert ly_path.is_file()
            assert f'Writing {ly_path.trim()} ...' in transcript
