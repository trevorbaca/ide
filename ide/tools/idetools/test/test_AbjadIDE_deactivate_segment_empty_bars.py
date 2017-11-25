import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_deactivate_segment_empty_bars_01():

    ly_paths = []
    for name in ('_', 'A', 'B'):
        ly_name = f'segment-{name}.ly'
        ly_path = ide.Path('red_score')._segments(ly_name)
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red lyee* q')
        transcript = abjad_ide.io.transcript
        for ly_path in ly_paths:
            line = f'No {ly_path.trim()} empty bars found ...'
            assert line in transcript


def test_AbjadIDE_deactivate_segment_empty_bars_02():

    abjad_ide('blu lyee* q')
    transcript = abjad_ide.io.transcript
    assert 'No _segments directory found ...' in transcript
