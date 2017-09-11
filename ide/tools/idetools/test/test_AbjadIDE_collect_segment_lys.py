import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_collect_segment_lys_01():

    ly_paths = []
    for number in ('01', '02', '03'):
        ly_name = f'segment-{number}.ly'
        ly_path = ide.Path('red_score').builds / '_segments' / ly_name
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red~score bb lyc q')
        transcript = abjad_ide.io.transcript
        for ly_path in ly_paths:
            assert ly_path.is_file()
            assert f'Writing {ly_path.trim()} ...' in transcript
