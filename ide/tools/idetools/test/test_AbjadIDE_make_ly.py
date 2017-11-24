import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        material = ide.Path('red_score', 'materials', 'red_pitch_classes')
        ly = material('illustration.ly')
        ly.remove()
        maker = material('__make_material_ly__.py')
        maker.remove()

        abjad_ide('red %rpc lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {ly.trim()} ...' not in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {ly.trim()} ...' not in transcript
        assert ly.is_file()
        assert not maker.exists()

        abjad_ide('red %rpc lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {ly.trim()} ...' in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {ly.trim()} ...' not in transcript
        assert ly.is_file()
        assert not maker.exists()


def test_AbjadIDE_make_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        segment = ide.Path('red_score', 'segments', 'A')
        ly = segment('illustration.ly')
        ly.remove()
        maker = segment('__make_segment_ly__.py')
        maker.remove()

        abjad_ide('red %A lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {ly.trim()} ...' not in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {ly.trim()} ...' not in transcript
        assert ly.is_file()
        assert not maker.exists()

        abjad_ide('red %A lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {ly.trim()} ...' in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Opening {ly.trim()} ...' not in transcript
        assert ly.is_file()
        assert not maker.exists()
