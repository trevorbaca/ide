import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_new_01():
    """
    Makes build directory.
    """

    build = ide.Path(scores, "red_score", "red_score", "builds", "arch-a-score")
    with ide.Test(remove=[build]):

        abjad_ide("red bb new score arch-a-score arch~a $80 ARCH-A y q")
        transcript = abjad_ide.io.transcript
        lines = transcript.lines
        assert build.is_dir()
        assert build.get_metadatum("price") == "$80"
        assert build.get_metadatum("catalog_number_suffix") == "ARCH-A"
        assert "Build name> arch-a-score" in lines
        assert "Paper size> arch a" in lines
        assert r"Price> $80" in lines
        assert "Catalog number suffix> ARCH-A" in lines
        index = lines.index("Ok?> y")
        assert lines[index:] == [
            "Ok?> y",
            "",
            "Writing red_score/builds/arch-a-score/back-cover.tex ...",
            "",
            "Writing red_score/builds/arch-a-score/front-cover.tex ...",
            "",
            "Writing red_score/builds/arch-a-score/layout.py ...",
            "",
            "Collecting segment lys ...",
            " Writing red_score/builds/arch-a-score/_segments/segment--.ily ...",
            " Writing red_score/builds/arch-a-score/_segments/segment--.ly ...",
            " Writing red_score/builds/arch-a-score/_segments/segment-A.ily ...",
            " Writing red_score/builds/arch-a-score/_segments/segment-A.ly ...",
            " Writing red_score/builds/arch-a-score/_segments/segment-B.ily ...",
            " Writing red_score/builds/arch-a-score/_segments/segment-B.ly ...",
            " Removing fermata measure numbers from metadata ...",
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
            "",
            "Generating red_score/builds/arch-a-score/music.ly ...",
            " Examining red_score/segments/_ ...",
            " Examining red_score/segments/A ...",
            " Examining red_score/segments/B ...",
            " Writing red_score/builds/arch-a-score/music.ly ...",
            "",
            "Writing red_score/builds/arch-a-score/preface.tex ...",
            "",
            "Generating score ...",
            "Writing red_score/builds/arch-a-score/score.tex ...",
            "",
            "Generating stylesheet ...",
            "Writing red_score/builds/arch-a-score/stylesheet.ily ...",
            "",
            "> q",
            "",
        ]

        abjad_ide("red bb new score arch-a-score q")
        transcript = abjad_ide.io.transcript
        assert f"Existing {build.trim()} ..." in transcript


def test_AbjadIDE_new_02():
    """
    Makes build directory. Ignores empty metadata.
    """

    path = ide.Path(scores, "red_score", "red_score", "builds", "arch-a-score")
    with ide.Test(remove=[path]):

        abjad_ide("red bb new score arch-a-score arch~a <return> <return> y q")
        transcript = abjad_ide.io.transcript
        assert path.is_dir()
        assert path.get_metadatum("price") is None
        assert path.get_metadatum("catalog_number_suffix") is None
        assert "Build name> arch-a-score" in transcript
        assert "Paper size> arch a" in transcript
        assert r"Price>" in transcript
        assert "Catalog number suffix>" in transcript
        assert "Making ..." in transcript
        assert f"    {path.trim()}" in transcript
        paths = [
            path / _
            for _ in (
                "back-cover.tex",
                "front-cover.tex",
                "music.ly",
                "preface.tex",
                "score.tex",
                "stylesheet.ily",
            )
        ]
        for path in paths:
            assert f"    {path.trim()}" in transcript
        assert "Ok?> y" in transcript
        assert "Generating score ..." in transcript
        assert "Generating stylesheet ..." in transcript
        for path in paths:
            assert f"Writing {path.trim()} ..." in transcript


def test_AbjadIDE_new_03():
    """
    Makes parts directory.
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
            " Writing green_score/builds/arch-a-parts/_segments/segment--.ly ...",
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
        assert (directory._segments / "segment--.ly").is_file()

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


def test_AbjadIDE_new_04():
    """
    Makes score package.
    """

    with ide.Test():

        abjad_ide("new Purple~Score q")
        transcript = abjad_ide.io.transcript
        wrapper = ide.Configuration().test_scores_directory / "purple_score"
        assert wrapper.is_dir()
        for name in [
            ".gitignore",
            ".travis.yml",
            "README.md",
            "purple_score",
            "requirements.txt",
            "setup.cfg",
            "setup.py",
        ]:
            assert (wrapper / name).exists()
        for name in [
            "__init__.py",
            "__metadata__.py",
            "builds",
            "distribution",
            "etc",
            "segments",
            "stylesheets",
            "test",
        ]:
            assert (wrapper.contents / name).exists()
        assert (wrapper.segments / "__init__.py").is_file()
        assert "Enter title> Purple Score" in transcript
        assert f"Making {wrapper.trim()} ..." in transcript

        assert wrapper.builds._assets.exists()
        assert (wrapper.builds._assets / ".gitignore").is_file()
        assert (wrapper.builds / "__metadata__.py").is_file()

        abjad_ide("new Purple~Score q")
        transcript = abjad_ide.io.transcript
        assert f"Existing {wrapper.trim()} ..." in transcript


def test_AbjadIDE_new_05():
    """
    Makes score package in empty directory.
    """

    with ide.Test():
        wrapper = ide.Configuration().test_scores_directory / "purple_score"
        wrapper.remove()
        wrapper.mkdir()
        assert wrapper.is_dir()
        git = wrapper / ".git"
        git.mkdir()
        assert git.is_dir()

        abjad_ide("new y Purple~Score q")
        transcript = abjad_ide.io.transcript
        assert wrapper.exists()
        for name in [
            ".travis.yml",
            "README.md",
            "requirements.txt",
            "setup.cfg",
            "setup.py",
        ]:
            assert (wrapper / name).exists()
        for name in [
            "__init__.py",
            "__metadata__.py",
            "builds",
            "distribution",
            "etc",
            "segments",
            "stylesheets",
            "test",
        ]:
            assert (wrapper.contents / name).exists()
        assert (wrapper.segments / "__init__.py").is_file()
        assert f"Found {wrapper.trim()}." in transcript
        assert f"Populate {wrapper.trim()}?>" in transcript
        assert "Enter title> Purple Score" in transcript
        assert f"Making {wrapper.trim()} ..." in transcript

        abjad_ide("new Purple~Score q")
        transcript = abjad_ide.io.transcript
        assert f"Existing {wrapper.trim()} ..." in transcript


def test_AbjadIDE_new_06():
    """
    Makes score package. Coerces package name.
    """

    package = ide.Configuration().test_scores_directory / "purple_score"

    with ide.Test(remove=[package]):

        abjad_ide("new PurpleScore q")
        assert package.is_dir()

    with ide.Test(remove=[package]):

        abjad_ide("new purpleScore q")
        assert package.is_dir()

    with ide.Test(remove=[package]):

        abjad_ide("new Purple_Score q")
        assert package.is_dir()

    with ide.Test(remove=[package]):

        abjad_ide("new purple_score q")
        assert package.is_dir()


def test_AbjadIDE_new_07():
    """
    Makes segment directory.
    """

    path = ide.Path(scores, "red_score", "red_score", "segments", "segment_04")
    with ide.Test(remove=[path]):

        abjad_ide("red gg new segment~04 q")
        transcript = abjad_ide.io.transcript
        assert path.is_dir()
        names = [
            "__init__.py",
            "__metadata__.py",
            "definition.py",
            "layout.py",
        ]
        for name in names:
            assert (path / name).is_file()
        assert "Enter package name> segment 04" in transcript
        assert f"Making {path.trim()} ..." in transcript
        for name in names:
            assert f"Writing {(path / name).trim()} ..." in transcript

        abjad_ide("red gg new segment_04 q")
        transcript = abjad_ide.io.transcript
        assert f"Existing {path.trim()} ..."


def test_AbjadIDE_new_08():
    """
    Makes stylesheet.
    """

    path = ide.Path(
        scores, "red_score", "red_score", "stylesheets", "new-stylesheet.ily"
    )
    with ide.Test(remove=[path]):

        abjad_ide("red yy new new~stylesheet y q")
        transcript = abjad_ide.io.transcript
        assert path.is_file()
        assert "File name> new stylesheet" in transcript
        assert f"Writing {path.trim()} ..." in transcript
        assert "Ok?> y" in transcript

        abjad_ide("red yy new new~stylesheet.ily q")
        transcript = abjad_ide.io.transcript
        assert f"Existing {path.trim()} ..."

        abjad_ide("red yy new <return> q")
        transcript = abjad_ide.io.transcript
        assert "Existing" not in transcript
        assert "Writing" not in transcript

        abjad_ide("red yy new ss q")
        transcript = abjad_ide.io.transcript
        assert "Existing" not in transcript
        assert "Writing" not in transcript
