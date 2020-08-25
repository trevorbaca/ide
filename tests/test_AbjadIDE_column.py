import pytest

import ide

abjad_ide = ide.AbjadIDE(test="dimensions=(10, 54)")


@pytest.mark.skip(reason="will fix soon")
def test_AbjadIDE_column_01():

    with ide.Test():

        abjad_ide(
            """
            red ee
            new test-file-01.txt y
            new test-file-02.txt y
            new test-file-03.txt y
            new test-file-04.txt y
            new test-file-05.txt y
            new test-file-06.txt y
            new test-file-07.txt y
            new test-file-08.txt y
            new test-file-09.txt y
            new test-file-10.txt y
            new test-file-11.txt y
            new test-file-12.txt y
            <return>
            q"""
        )
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
