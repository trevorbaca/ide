import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_new_01():
    r'''Makes new score directory.
    '''

    wrapper_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'green_score',
        )
    contents_directory = pathlib.Path(
        wrapper_directory,
        'green_score',
        )
    materials_directory = pathlib.Path(
        contents_directory,
        'materials',
        )
    segments_directory = pathlib.Path(
        contents_directory,
        'segments',
        )
    wrapper_directory_entries = [
        '.travis.yml',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        ]
    contents_directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'build',
        'distribution',
        'etc',
        'tools',
        'materials',
        'segments',
        'stylesheets',
        'test',
        ]
    materials_directory_entries = [
        '__init__.py',
        ]
    segments_directory_entries = [
        '__init__.py',
        ]

    input_ = 'new Green~Score q'

    with ide.Test():
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert wrapper_directory.is_dir()
        for entry in wrapper_directory_entries:
            path = pathlib.Path(wrapper_directory, entry)
            assert path.exists()
        for entry in contents_directory_entries:
            path = pathlib.Path(contents_directory, entry)
            assert path.exists()
        for entry in materials_directory_entries:
            path = pathlib.Path(materials_directory, entry)
            assert path.exists()
        for entry in segments_directory_entries:
            path = pathlib.Path(segments_directory, entry)
            assert path.exists()

    assert 'Enter title]> Green Score' in contents


def test_AbjadIDE_new_02():
    r'''Makes new score directory in preexisting empty directory.
    '''

    wrapper_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'green_score',
        )
    contents_directory = pathlib.Path(
        wrapper_directory,
        'green_score',
        )
    materials_directory = pathlib.Path(
        contents_directory,
        'materials',
        )
    segments_directory = pathlib.Path(
        contents_directory,
        'segments',
        )
    wrapper_directory_entries = [
        '.travis.yml',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        ]
    contents_directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'build',
        'distribution',
        'etc',
        'tools',
        'materials',
        'segments',
        'stylesheets',
        'test',
        ]
    materials_directory_entries = [
        '__init__.py',
        ]
    segments_directory_entries = [
        '__init__.py',
        ]

    input_ = 'new y Green~Score q'

    if wrapper_directory.exists():
        wrapper_directory.rmdir()

    with ide.Test():
        assert not wrapper_directory.exists()
        wrapper_directory.mkdir()
        git_directory = pathlib.Path(wrapper_directory, '.git')
        git_directory.mkdir()
        assert wrapper_directory.is_dir()
        assert git_directory.is_dir()
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert wrapper_directory.exists()
        for entry in wrapper_directory_entries:
            path = pathlib.Path(wrapper_directory, entry)
            assert path.exists()
        for entry in contents_directory_entries:
            path = pathlib.Path(contents_directory, entry)
            assert path.exists()
        for entry in materials_directory_entries:
            path = pathlib.Path(materials_directory, entry)
            assert path.exists()
        for entry in segments_directory_entries:
            path = pathlib.Path(segments_directory, entry)
            assert path.exists()

    assert 'Found' in contents
    assert 'Enter title]> Green Score' in contents


def test_AbjadIDE_new_03():
    r'''Coerces score directory name.
    '''

    score_package = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'green_score',
        )

    with ide.Test(remove=[score_package]):
        input_ = 'new GreenScore q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()

    with ide.Test(remove=[score_package]):
        input_ = 'new greenScore q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()

    with ide.Test(remove=[score_package]):
        input_ = 'new Green_Score q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()

    with ide.Test(remove=[score_package]):
        input_ = 'new green_score q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()


def test_AbjadIDE_new_04():
    r'''Makes new build subdirectory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'arch-a',
        )

    input_ = 'red~score bb new arch-a arch~a $80 ARCH-A y q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()


def test_AbjadIDE_new_05():
    r'''Coerces build subdirectory name.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'arch-a',
        )

    input_ = 'red~score bb new arch_a arch~a $80 ARCH-A y q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()


def test_AbjadIDE_new_06():
    r'''Makes new maker classfile.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'NewMaker.py',
        )

    input_ = 'red~score oo new NewMaker.py q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        string = path.read_text()
        assert 'class NewMaker(abjad.AbjadObject)' in string


def test_AbjadIDE_new_07():
    r'''Coerces maker classfile name.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'NewMaker.py',
        )

    input_ = 'red~score oo new New~Maker q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        string = path.read_text()
        assert 'class NewMaker(abjad.AbjadObject)' in string


def test_AbjadIDE_new_08():
    r'''Makes new maker functionfile.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'make_material.py',
        )

    input_ = 'red~score oo new make_material.py q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        string = path.read_text()
        assert 'def make_material():' in string


def test_AbjadIDE_new_09():
    r'''Coerces maker functionfile name.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'make_material.py',
        )

    input_ = 'red~score oo new make~material q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        string = path.read_text()
        assert 'def make_material():' in string


def test_AbjadIDE_new_10():
    r'''Makes new material directory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'test_notes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'Red~Score mm new test_notes q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_11():
    r'''Coerces material directory name.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'test_notes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'Red~Score mm new test~notes q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_12():
    r'''Makes new segment directory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'red~score gg new segment_04 q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_13():
    r'''Coerces segment directory name.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'red~score gg new segment~04 q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_14():
    r'''Makes new stylesheet.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'stylesheets',
        'new-stylesheet.ily',
        )

    input_ = 'red~score yy new new-stylesheet.ily q'

    with ide.Test():
        if path.exists():
            path.unlink()
        abjad_ide._start(input_=input_)
        assert path.exists()


def test_AbjadIDE_new_15():
    r'''Coerces stylesheet new.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'stylesheets',
        'new-stylesheet.ily',
        )

    input_ = 'red~score yy new new~stylesheet q'

    with ide.Test(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
