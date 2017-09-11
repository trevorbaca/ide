import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_paste_from_clipboard_01():

    with ide.Test():
        source = ide.Path('red_score').distribution
        source /= 'red-score-program-notes.txt'
        assert source.is_file()
        target_1 = ide.Path('blue_score').distribution
        target_1 /= 'red-score-program-notes.txt'
        target_1.remove()
        target_2 = target_1.with_name('new-notes.txt')
        target_2.remove()

        abjad_ide('red dd pc gram-no ss blue dd pv q')
        transcript = abjad_ide.io.transcript
        assert source in abjad_ide._clipboard
        assert target_1.is_file()
        assert 'Select files for clipboard> gram-no' in transcript
        assert 'Copying to clipboard ...' in transcript
        assert source.trim() in transcript
        assert 'Pasting from clipboard ...' in transcript
        assert target_1.trim() in transcript

        abjad_ide('red dd pc gram-no ss blue dd pv new-notes.txt q')
        transcript = abjad_ide.io.transcript
        assert target_2.is_file()
        assert 'Select files for clipboard> gram-no' in transcript
        assert 'Copying to clipboard ...' in transcript
        assert source.trim() in transcript
        assert 'Pasting from clipboard ...' in transcript
        assert target_1.trim() in transcript
        assert f'Existing {target_1.trim()} ...' in transcript
        assert 'Enter new name> new-notes.txt' in transcript
        assert target_2.trim() in transcript
