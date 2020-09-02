import ide

abjad_ide = ide.AbjadIDE(test="dimensions=(10, 54)")


def test_AbjadIDE_column_01():

    with ide.Test():

        directory = ide.configuration.test_scores_directory / "red_score" / "red_score"
        directory /= "etc"

        for i in range(12):
            i += 1
            name = f"test-file-{str(i).zfill(2)}.txt"
            path = directory / name
            path.touch()

        abjad_ide("red ee q")
        transcript = abjad_ide.io.transcript
        for line in [
            "   1: notes.txt               8: test-file-07.txt",
            "   2: test-file-01.txt        9: test-file-08.txt",
            "   3: test-file-02.txt       10: test-file-09.txt",
            "   4: test-file-03.txt       11: test-file-10.txt",
            "   5: test-file-04.txt       12: test-file-11.txt",
            "   6: test-file-05.txt       13: test-file-12.txt",
            "   7: test-file-06.txt",
        ]:
            assert line in transcript.lines, repr(line)

        abjad_ide("red ee ; q")
        transcript = abjad_ide.io.transcript
        for line in [
            "   1: notes.txt",
            "   2: test-file-01.txt",
            "   3: test-file-02.txt",
            "   4: test-file-03.txt",
            "   5: test-file-04.txt",
            "   6: test-file-05.txt",
            "   7: test-file-06.txt",
            "   8: test-file-07.txt",
            "   9: test-file-08.txt",
            "  10: test-file-09.txt",
            "  11: test-file-10.txt",
            "  12: test-file-11.txt",
            "  13: test-file-12.txt",
        ]:
            assert line in transcript.lines, repr(transcript.lines[-11][:])
