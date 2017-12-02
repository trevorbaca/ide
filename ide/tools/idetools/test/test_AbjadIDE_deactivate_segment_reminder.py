import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_deactivate_segment_reminder_01():

    ly_paths = []
    for name in ('_', 'A', 'B'):
        ly_name = f'segment-{name}.ly'
        ly_path = ide.Path('red_score')._segments(ly_name)
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red %let srex q')
        transcript = abjad_ide.io.transcript
        tag = 'SEGMENT:REMINDER'
        for ly_path in ly_paths:
            line = f'Deactivating 0 {tag} tags in {ly_path.name} ...'
            assert line in transcript


def test_AbjadIDE_deactivate_segment_reminder_02():

    abjad_ide('blu %let srex q')
    transcript = abjad_ide.io.transcript
    assert 'No _segments directory found ...' in transcript
