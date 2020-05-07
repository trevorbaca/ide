import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_duplicate_01():
    """
    In build directory.
    """

    abjad_ide(f"red %let dup layout.ly q")
    transcript = abjad_ide.io.transcript
    assert "Select files to duplicate> layout.ly" in transcript
    assert "Duplicating red_score/builds/letter-score/layout.ly ..." in transcript
    assert "Enter new name> q" in transcript


def test_AbjadIDE_duplicate_02():
    """
    In distribution directory.
    """

    abjad_ide(f"red dd dup red-score.pdf q")
    transcript = abjad_ide.io.transcript
    assert "Select files to duplicate> red-score.pdf" in transcript
    assert "Duplicating red_score/distribution/red-score.pdf ..." in transcript
    assert "Enter new name> q" in transcript


def test_AbjadIDE_duplicate_03():
    """
    In etc directory.
    """

    abjad_ide(f"red ee dup notes.txt q")
    transcript = abjad_ide.io.transcript
    assert "Select files to duplicate> notes.txt" in transcript
    assert "Duplicating red_score/etc/notes.txt ..." in transcript
    assert "Enter new name> q" in transcript


def test_AbjadIDE_duplicate_04():
    """
    In materials directory.
    """

    with ide.Test():
        source = ide.Path("red_score", "materials", "red_pitch_classes")
        assert source.is_dir()
        target = source.with_name("orange_pitch_classes")
        target.remove()

        abjad_ide(f"red mm dup rpc orange~pitch~classes y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f"Select packages to duplicate> rpc" in transcript
        assert f"Duplicating {source.trim()} ..."
        assert "Enter new name> orane pitch classes"
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        line = "Replacing 'red_pitch_classes' with 'orange_pitch_classes' ..."
        assert line in transcript


def test_AbjadIDE_duplicate_05():
    """
    In scores directory.
    """

    with ide.Test():
        source = ide.Path("red_score").wrapper
        assert source.is_dir()
        target = source.with_name("purple_score")
        target.remove()

        abjad_ide("dup red Purple~Score y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert "Select packages to duplicate> red" in transcript
        assert f"Duplicating {source.trim()} ..." in transcript
        assert "Enter title> Purple Score" in transcript
        assert "Ok?> y" in transcript
        assert "Replacing 'red_score' with 'purple_score' ..." in transcript
        assert "Replacing 'Red Score' with 'Purple Score' ..." in transcript


def test_AbjadIDE_duplicate_06():
    """
    In scores directory. Handles empty return gracefully.
    """

    abjad_ide("dup <return> q")
    transcript = abjad_ide.io.transcript
    assert "Select packages to duplicate> " in transcript


def test_AbjadIDE_duplicate_07():
    """
    In segments directory.
    """

    with ide.Test():
        source = ide.Path("blue_score", "segments", "A")
        assert source.is_dir()
        target = source.with_name("B")
        target.remove()

        abjad_ide(f"blu gg dup A B y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f"Select packages to duplicate> A" in transcript
        assert f"Duplicating {source.trim()} ..."
        assert "Enter new name> B"
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
        assert "Replacing 'A' with 'B' ..." in transcript


def test_AbjadIDE_duplicate_08():
    """
    In stylesheets directory.
    """

    with ide.Test():
        source = ide.Path("red_score", "stylesheets", "stylesheet.ily")
        assert source.is_file()
        target = source.with_name("new-stylesheet.ily")
        target.remove()

        abjad_ide(f"red yy dup eet.i new~stylesheet y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f"Select files to duplicate> eet.i" in transcript
        assert f"Duplicating {source.trim()} ..." in transcript
        assert "Enter new name> new stylesheet" in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript


def test_AbjadIDE_duplicate_09():
    """
    In test directory.
    """

    with ide.Test():
        source = ide.Path("red_score", "test", "test_materials.py")
        assert source.is_file()
        target = source.with_name("test_new_materials.py")
        target.remove()

        abjad_ide(f"red tt dup _mat test~new~materials y q")
        transcript = abjad_ide.io.transcript
        assert target.exists()
        assert f"Select files to duplicate> _mat" in transcript
        assert f"Duplicating {source.trim()} ..." in transcript
        assert "Enter new name> test new materials" in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript


def test_AbjadIDE_duplicate_10():
    """
    In tools directory.
    """

    with ide.Test():
        source = ide.Path("red_score", "tools", "ScoreTemplate.py")
        assert source.is_file()
        target = source.with_name("ColorSpecifier.py")
        target.remove()

        abjad_ide(f"red oo dup ST Color~specifier y q")
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f"Select files to duplicate> ST" in transcript
        assert f"Duplicating {source.trim()} ..." in transcript
        assert "Enter new name> Color specifier" in transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert "Ok?> y" in transcript
