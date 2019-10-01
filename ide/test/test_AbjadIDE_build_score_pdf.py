import ide
import os
import pytest

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_build_score_pdf_01():

    with ide.Test():
        abjad_ide("red %let spb q")
        lines = abjad_ide.io.transcript.lines
        index = lines.index("Building score ...")
        assert lines[index:] == [
            "Building score ...",
            "Preparing red_score/builds/letter-score/music.ly ...",
            "Collecting segment lys ...",
            " Writing red_score/builds/letter-score/_segments/segment--.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment--.ly ...",
            " Writing red_score/builds/letter-score/_segments/segment-A.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-A.ly ...",
            " Writing red_score/builds/letter-score/_segments/segment-B.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-B.ly ...",
            "Handling edition tags ...",
            " Found no other-edition tags ...",
            " Found no this-edition tags ...",
            "Handling fermata bar lines ...",
            " Found no bar line adjustment tags ...",
            " Found no EOL fermata bar line tags ...",
            "Handling shifted clefs ...",
            " Found no shifted clef tags ...",
            " Found no BOL clef tags ...",
            "Handling MOL tags ...",
            " Found no MOL tags ...",
            " Found no conflicting MOL tags ...",
            "Uncoloring persistent indicators ...",
            " Found no persistent indicator color suppression tags ...",
            " Found no persistent indicator color expression tags ...",
            "Hiding music annotations ...",
            " Found no music annotation tags ...",
            " Found no music annotation tags ...",
            "Joining broken spanners ...",
            " Found no broken spanner expression tags ...",
            " Found no broken spanner suppression tags ...",
            "Showing PHANTOM tags ...",
            " Found no PHANTOM tags ...",
            "Hiding PHANTOM tags ...",
            " Found no PHANTOM tags ...",
            "Showing EOS_STOP_MM_SPANNER tags ...",
            " Found no EOS_STOP_MM_SPANNER tags ...",
            "Generating red_score/builds/letter-score/music.ly ...",
            " Removing red_score/builds/letter-score/music.ly ...",
            " Examining red_score/segments/_ ...",
            " Examining red_score/segments/A ...",
            " Examining red_score/segments/B ...",
            " Writing red_score/builds/letter-score/music.ly ...",
            "Interpreting red_score/builds/letter-score/music.ly ...",
            "Found red_score/builds/letter-score/music.pdf ...",
            "",
            "Interpreting red_score/builds/letter-score/front-cover.tex ...",
            "Found red_score/builds/letter-score/front-cover.pdf ...",
            "",
            "Interpreting red_score/builds/letter-score/preface.tex ...",
            "Found red_score/builds/letter-score/preface.pdf ...",
            "",
            "Interpreting red_score/builds/letter-score/back-cover.tex ...",
            "Found red_score/builds/letter-score/back-cover.pdf ...",
            "",
            "Generating score ...",
            "Removing red_score/builds/letter-score/score.tex ...",
            "Writing red_score/builds/letter-score/score.tex ...",
            "",
            "Interpreting red_score/builds/letter-score/score.tex ...",
            "Found red_score/builds/letter-score/score.pdf ...",
            "Opening red_score/builds/letter-score/score.pdf ...",
            "",
            "> q",
            "",
        ]
