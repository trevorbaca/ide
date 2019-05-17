import ide

abjad_ide = ide.AbjadIDE(test="dimensions=(10, 54)")


def test_AbjadIDE_column_01():

    with ide.Test():

        abjad_ide(
            """
            red oo
            new test_file_01.py y
            new test_file_02.py y
            new test_file_03.py y
            new test_file_04.py y
            new test_file_05.py y
            new test_file_06.py y
            new test_file_07.py y
            new test_file_08.py y
            new test_file_09.py y
            new test_file_10.py y
            new test_file_11.py y
            new test_file_12.py y
            <return>
            q"""
        )
        transcript = abjad_ide.io.transcript
        for line in [
            "   1: PianoStaffSegmentMaker.py     9: test_file_05.py",
            "   2: RhythmMaker.py               10: test_file_06.py",
            "   3: ScoreTemplate.py             11: test_file_07.py",
            "   4: adjust_spacing_sections.py   12: test_file_08.py",
            "   5: test_file_01.py              13: test_file_09.py",
            "   6: test_file_02.py              14: test_file_10.py",
            "   7: test_file_03.py              15: test_file_11.py",
            "   8: test_file_04.py              16: test_file_12.py",
        ]:
            assert line in transcript.lines, repr(line)

        abjad_ide("red oo ; q")
        transcript = abjad_ide.io.transcript
        for line in [
            "   1: PianoStaffSegmentMaker.py",
            "   2: RhythmMaker.py",
            "   3: ScoreTemplate.py",
            "   4: adjust_spacing_sections.py",
            "   5: test_file_01.py",
            "   6: test_file_02.py",
            "   7: test_file_03.py",
            "   8: test_file_04.py",
            "   9: test_file_05.py",
            "  10: test_file_06.py",
            "  11: test_file_07.py",
            "  12: test_file_08.py",
            "  13: test_file_09.py",
            "  14: test_file_10.py",
            "  15: test_file_11.py",
            "  16: test_file_12.py",
        ]:
            assert line in transcript.lines, repr(transcript.lines[-11][:])
