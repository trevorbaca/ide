import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_new_01():
    """
    Makes parts build directory.
    """

    with ide.Test():
        directory = ide.Path(
            scores, "green_score", "green_score", "builds", "arch-a-parts"
        )
        assert not directory.exists()

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y q")
        transcript = abjad_ide.io.transcript
        lines = transcript.lines
        assert "Getting part names from score template ..." in lines
        assert "Found BassClarinet ..." in lines
        assert "Found Violin ..." in lines
        assert "Found Viola ..." in lines
        assert "Found Cello ..." in lines

        assert "Directory name> arch-a-parts" in lines
        assert "Paper size> arch a" in lines
        assert "Catalog number suffix> ARCH-A" in lines
        assert "Will make ..." in lines
        for line in [
            "    green_score/builds/arch-a-parts",
            "    green_score/builds/arch-a-parts/stylesheet.ily",
            "    green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-front-cover.tex",
            "    green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-preface.tex",
            "    green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-music.ly",
            "    green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-back-cover.tex",
            "    green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-part.tex",
            "    green_score/builds/arch-a-parts/violin/violin-front-cover.tex",
            "    green_score/builds/arch-a-parts/violin/violin-preface.tex",
            "    green_score/builds/arch-a-parts/violin/violin-music.ly",
            "    green_score/builds/arch-a-parts/violin/violin-back-cover.tex",
            "    green_score/builds/arch-a-parts/violin/violin-part.tex",
            "    green_score/builds/arch-a-parts/viola/viola-front-cover.tex",
            "    green_score/builds/arch-a-parts/viola/viola-preface.tex",
            "    green_score/builds/arch-a-parts/viola/viola-music.ly",
            "    green_score/builds/arch-a-parts/viola/viola-back-cover.tex",
            "    green_score/builds/arch-a-parts/viola/viola-part.tex",
            "    green_score/builds/arch-a-parts/cello/cello-front-cover.tex",
            "    green_score/builds/arch-a-parts/cello/cello-preface.tex",
            "    green_score/builds/arch-a-parts/cello/cello-music.ly",
            "    green_score/builds/arch-a-parts/cello/cello-back-cover.tex",
            "    green_score/builds/arch-a-parts/cello/cello-part.tex",
        ]:
            assert line in lines, repr(line)

        assert "Ok?> y" in lines

        for line in [
            "Collecting segment lys ...",
            " Writing green_score/builds/arch-a-parts/_segments/segment-01.ly ...",
            " Writing fermata measure numbers to metadata ...",
            " Writing time signatures to metadata ...",
            "Handling build tags ...",
            " Handling edition tags ...",
            "  Found no other-edition tags ...",
            "  Found no this-edition tags ...",
            " Handling fermata bar lines ...",
            "  Found no bar line adjustment tags ...",
            " Handling shifted clefs ...",
            "  Found no shifted clef tags ...",
            " Handling MOL tags ...",
            "  Found no MOL tags ...",
            " Uncoloring persistent indicators ...",
            "  Found 1 persistent indicator color suppression tag ...",
            "  Activating 1 persistent indicator color suppression tag ...",
            "  Found 30 persistent indicator color expression tags ...",
            "  Deactivating 26 persistent indicator color expression tags ...",
            "  Skipping 4 (inactive) persistent indicator color expression tags ...",
            " Hiding music annotations ...",
            "  Found no music annotation tags ...",
            "  Found 3 music annotation tags ...",
            "  Deactivating 1 music annotation tag ...",
            "  Skipping 2 (inactive) music annotation tags ...",
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
            "Generating stylesheet ...",
            "Writing green_score/builds/arch-a-parts/stylesheet.ily ...",
            "Writing"
            " green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-back-cover.tex ...",
            "Writing"
            " green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-front-cover.tex ...",
            "Generating"
            " green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-music.ly ...",
            " Writing"
            " green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-music.ly ...",
            "Writing"
            " green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-part.tex ...",
            "Writing"
            " green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-preface.tex ...",
            "Writing"
            " green_score/builds/arch-a-parts/bass-clarinet/bass_clarinet_layout.py ...",
            "Writing green_score/builds/arch-a-parts/violin/violin-back-cover.tex ...",
            "Writing green_score/builds/arch-a-parts/violin/violin-front-cover.tex ...",
            "Generating green_score/builds/arch-a-parts/violin/violin-music.ly ...",
            " Writing green_score/builds/arch-a-parts/violin/violin-music.ly ...",
            "Writing green_score/builds/arch-a-parts/violin/violin-part.tex ...",
            "Writing green_score/builds/arch-a-parts/violin/violin-preface.tex ...",
            "Writing green_score/builds/arch-a-parts/violin/violin_layout.py ...",
            "Writing green_score/builds/arch-a-parts/viola/viola-back-cover.tex ...",
            "Writing green_score/builds/arch-a-parts/viola/viola-front-cover.tex ...",
            "Generating green_score/builds/arch-a-parts/viola/viola-music.ly ...",
            " Writing green_score/builds/arch-a-parts/viola/viola-music.ly ...",
            "Writing green_score/builds/arch-a-parts/viola/viola-part.tex ...",
            "Writing green_score/builds/arch-a-parts/viola/viola-preface.tex ...",
            "Writing green_score/builds/arch-a-parts/viola/viola_layout.py ...",
            "Writing green_score/builds/arch-a-parts/cello/cello-back-cover.tex ...",
            "Writing green_score/builds/arch-a-parts/cello/cello-front-cover.tex ...",
            "Generating green_score/builds/arch-a-parts/cello/cello-music.ly ...",
            " Writing green_score/builds/arch-a-parts/cello/cello-music.ly ...",
            "Writing green_score/builds/arch-a-parts/cello/cello-part.tex ...",
            "Writing green_score/builds/arch-a-parts/cello/cello-preface.tex ...",
            "Writing green_score/builds/arch-a-parts/cello/cello_layout.py ...",
        ]:
            assert line in lines, repr(line)

        assert directory.is_parts()
        assert (directory / "__metadata__.py").is_file()
        assert directory._assets.exists()
        assert (directory._assets / ".gitignore").is_file()
        assert directory._segments.exists()
        assert (directory._segments / ".gitignore").is_file()
        assert (directory._segments / "segment-01.ly").is_file()

        for name in [
            "bass-clarinet-back-cover.tex",
            "bass-clarinet-front-cover.tex",
            "bass-clarinet-music.ly",
            "bass-clarinet-part.tex",
            "bass-clarinet-preface.tex",
            "bass_clarinet_layout.py",
        ]:
            path = directory / "bass-clarinet" / name
            assert path.is_file()

        for name in [
            "cello-back-cover.tex",
            "cello-front-cover.tex",
            "cello-music.ly",
            "cello-part.tex",
            "cello-preface.tex",
            "cello_layout.py",
        ]:
            path = directory / "cello" / name
            assert path.is_file()

        for name in [
            "viola-back-cover.tex",
            "viola-front-cover.tex",
            "viola-music.ly",
            "viola-part.tex",
            "viola-preface.tex",
            "viola_layout.py",
        ]:
            path = directory / "viola" / name
            assert path.is_file()

        for name in [
            "violin-back-cover.tex",
            "violin-front-cover.tex",
            "violin-music.ly",
            "violin-part.tex",
            "violin-preface.tex",
            "violin_layout.py",
        ]:
            path = directory / "violin" / name
            assert path.is_file(), repr(path)

        stylesheet = directory / "stylesheet.ily"
        assert stylesheet.is_file()
