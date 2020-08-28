import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_paste_from_clipboard_01():

    with ide.Test():
        source = ide.Path(scores, "red_score", "red_score").distribution
        source /= "red-score-program-notes.txt"
        assert source.is_file()
        target_1 = ide.Path(scores, "blue_score", "blue_score").distribution
        target_1 /= "red-score-program-notes.txt"
        target_1.remove()
        target_2 = target_1.with_name("new-notes.txt")
        target_2.remove()

        abjad_ide("red dd cbc gram-no ss blue dd cbv q")
        transcript = abjad_ide.io.transcript
        assert target_1.is_file()
        assert "Select files for clipboard> gram-no" in transcript
        assert "Copying to clipboard ..." in transcript
        assert source.trim() in transcript
        assert "Pasting from clipboard ..." in transcript
        assert target_1.trim() in transcript
