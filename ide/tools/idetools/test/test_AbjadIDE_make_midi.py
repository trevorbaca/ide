import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_midi_01():

    with ide.Test():
        target = ide.Path('red_score').segments / 'segment_01'
        target /= 'segment.midi'
        maker = target.with_name('__midi__.py')
        target.remove()

        abjad_ide('red~score %A midim q')
        transcript = abjad_ide.io.transcript
        assert 'Making MIDI ...'in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red~score %A midim q')
        transcript = abjad_ide.io.transcript
        assert 'Making MIDI ...'in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Removing {maker.trim()} ...' in transcript
        assert f'Writing {maker.trim()} ...' in transcript
        assert f'Interpreting {maker.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
