import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_make_segment_midi_01():

    with ide.Test():
        directory = ide.Path(scores, "red_score", "red_score", "segments", "01")
        midi = directory / "segment.midi"
        midi.remove()
        maker = directory / "__make_segment_midi__.py"
        maker.remove()

        abjad_ide("red gg 01 midm q")
        transcript = abjad_ide.io.transcript
        assert "Making MIDI ..." in transcript
        assert f"Removing {midi.trim()} ..." not in transcript
        assert f"Writing {maker.trim()} ..." in transcript
        assert f"Interpreting {maker.trim()} ..." in transcript
        assert f"Found {midi.trim()} ..." in transcript
        assert f"Removing {maker.trim()} ..." in transcript
        assert f"Opening {midi.trim()} ..." in transcript
        assert midi.is_file()
        assert not maker.exists()

        abjad_ide("red gg 01 midm q")
        transcript = abjad_ide.io.transcript
        assert "Making MIDI ..." in transcript
        assert f"Removing {midi.trim()} ..." in transcript
        assert f"Writing {maker.trim()} ..." in transcript
        assert f"Interpreting {maker.trim()} ..." in transcript
        assert f"Found {midi.trim()} ..." in transcript
        assert f"Removing {maker.trim()} ..." in transcript
        assert f"Opening {midi.trim()} ..." in transcript
        assert midi.is_file()
        assert not maker.exists()
