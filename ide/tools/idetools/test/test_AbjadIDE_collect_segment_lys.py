import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_collect_segment_lys_01():

    ly_paths = []
    for number in ('01', '02', '03'):
        ly_name = 'segment-{}.ly'
        ly_name = ly_name.format(number)
        ly_path = ide.Path('red_score')
        ly_path = ly_path / 'build' / '_segments' / ly_name
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):
        input_ = 'red~score bb lyc q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        for ly_path in ly_paths:
            assert ly_path.is_file()

    for ly_path in ly_paths:
        message = f'Writing {abjad_ide._trim(ly_path)} ...'
        assert message in contents
