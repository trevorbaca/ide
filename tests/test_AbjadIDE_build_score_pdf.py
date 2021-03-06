import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_build_score_pdf_01():

    scores = ide.configuration.test_scores_directory
    source = ide.Path(scores, "red_score", "red_score", "builds", "letter-score")

    _segments = source / "_segments"
    for file_ in _segments.glob("*.ily"):
        file_.remove()
    for file_ in _segments.glob("*.ly"):
        file_.remove()

    pdfs = list(source.glob("*.pdf"))
    for pdf in pdfs:
        pdf.remove()

    with ide.Test():
        abjad_ide("red bb let spb q")
        lines = abjad_ide.io.transcript.lines
        index = lines.index("Building score ...")
        assert lines[index:] == [
            "Building score ...",
            "Interpreting red_score/builds/letter-score music.ly files ...",
            "Found red_score/builds/letter-score/music.ly ...",
            "Collecting segment lys ...",
            " Writing red_score/builds/letter-score/_segments/segment-01.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-01.ly ...",
            " Writing red_score/builds/letter-score/_segments/segment-02.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-02.ly ...",
            " Writing red_score/builds/letter-score/_segments/segment-03.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-03.ly ...",
            " Removing fermata measure numbers from metadata ...",
            " Writing time signatures to metadata ...",
            "Handling build tags ...",
            " Handling edition tags ...",
            "  Found no other-edition tags ...",
            "  Found no this-edition tags ...",
            " Handling fermata bar lines ...",
            "  Found no bar line adjustment tags ...",
            "  Found no EOL fermata bar line tags ...",
            " Handling shifted clefs ...",
            "  Found no shifted clef tags ...",
            "  Found no BOL clef tags ...",
            " Handling MOL tags ...",
            "  Found no MOL tags ...",
            "  Found no conflicting MOL tags ...",
            " Uncoloring persistent indicators ...",
            "  Found no persistent indicator color suppression tags ...",
            "  Found no persistent indicator color expression tags ...",
            " Hiding music annotations ...",
            "  Found no music annotation tags ...",
            "  Found no music annotation tags ...",
            " Joining broken spanners ...",
            "  Found no broken spanner expression tags ...",
            "  Found no broken spanner suppression tags ...",
            " Hiding left-broken-should-deactivate tags ...",
            "  Found no left-broken-should-deactivate tags ...",
            " Showing PHANTOM tags ...",
            "  Found no PHANTOM tags ...",
            " Hiding PHANTOM tags ...",
            "  Found no PHANTOM tags ...",
            " Showing phantom-should-activate tags ...",
            "  Found no phantom-should-activate tags ...",
            " Hiding phantom-should-deactivate tags ...",
            "  Found no phantom-should-deactivate tags ...",
            " Showing EOS_STOP_MM_SPANNER tags ...",
            "  Found no EOS_STOP_MM_SPANNER tags ...",
            " Hiding METRIC_MODULATION_IS_STRIPPED tags ...",
            "  Found no METRIC_MODULATION_IS_STRIPPED tags ...",
            " Hiding METRIC_MODULATION_IS_SCALED tags ...",
            "  Found no METRIC_MODULATION_IS_SCALED tags ...",
            "Checking layout time signatures ...",
            " Found red_score/builds/letter-score/layout.ly ...",
            " Found time signature metadata ...",
            " Layout time signatures (11) match metadata time signatures (11) ...",
            "Running LilyPond on red_score/builds/letter-score/music.ly ...",
            " Interpreting red_score/builds/letter-score/music.ly ...",
            "ERROR IN LILYPOND LOG FILE ...",
            " Found red_score/builds/letter-score/music.pdf ...",
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
