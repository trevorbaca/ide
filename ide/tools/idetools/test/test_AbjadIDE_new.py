import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_new_01():
    r'''Makes new score directory.
    '''

    outer_score_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score',
        )
    inner_score_directory = pathlib.Path(
        outer_score_directory,
        'example_score',
        )
    materials_directory = pathlib.Path(
        inner_score_directory,
        'materials',
        )
    segments_directory = pathlib.Path(
        inner_score_directory,
        'segments',
        )
    outer_directory_entries = [
        '.travis.yml',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        ]
    inner_directory_entries = [
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
        #'__abbreviations__.py',
        '__init__.py',
        #'__metadata__.py',
        #'__views__.py',
        ]
    segments_directory_entries = [
        '__init__.py',
        #'__metadata__.py',
        #'__views__.py',
        ]

    input_ = 'new Example~Score q'

    with abjad.FilesystemState(remove=[outer_score_directory]):
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert outer_score_directory.is_dir()
        for entry in outer_directory_entries:
            path = pathlib.Path(outer_score_directory, entry)
            assert path.exists()
        for entry in inner_directory_entries:
            path = pathlib.Path(inner_score_directory, entry)
            assert path.exists()
        for entry in materials_directory_entries:
            path = pathlib.Path(materials_directory, entry)
            assert path.exists()
        for entry in segments_directory_entries:
            path = pathlib.Path(segments_directory, entry)
            assert path.exists()

    assert 'Enter title]> Example Score' in contents


def test_AbjadIDE_new_02():
    r'''Makes new score directory in preexisting empty directory.
    '''

    outer_score_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score',
        )
    inner_score_directory = pathlib.Path(
        outer_score_directory,
        'example_score',
        )
    materials_directory = pathlib.Path(
        inner_score_directory,
        'materials',
        )
    segments_directory = pathlib.Path(
        inner_score_directory,
        'segments',
        )
    outer_directory_entries = [
        '.travis.yml',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        ]
    inner_directory_entries = [
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
        #'__abbreviations__.py',
        '__init__.py',
        #'__metadata__.py',
        #'__views__.py',
        ]
    segments_directory_entries = [
        '__init__.py',
        #'__metadata__.py',
        #'__views__.py',
        ]

    input_ = 'new y Example~Score q'

    if outer_score_directory.exists():
        outer_score_directory.rmdir()

    with abjad.FilesystemState(remove=[outer_score_directory]):
        assert not outer_score_directory.exists()
        outer_score_directory.mkdir()
        git_directory = pathlib.Path(outer_score_directory, '.git')
        git_directory.mkdir()
        assert outer_score_directory.is_dir()
        assert git_directory.is_dir()
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert outer_score_directory.exists()
        for entry in outer_directory_entries:
            path = pathlib.Path(outer_score_directory, entry)
            assert path.exists()
        for entry in inner_directory_entries:
            path = pathlib.Path(inner_score_directory, entry)
            assert path.exists()
        for entry in materials_directory_entries:
            path = pathlib.Path(materials_directory, entry)
            assert path.exists()
        for entry in segments_directory_entries:
            path = pathlib.Path(segments_directory, entry)
            assert path.exists()

    assert 'Found' in contents
    assert 'Enter title]> Example Score' in contents


def test_AbjadIDE_new_03():
    r'''Coerces score directory name.
    '''

    score_package = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_1',
        )

    with abjad.FilesystemState(remove=[score_package]):
        input_ = 'new ExampleScore1 q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()

    with abjad.FilesystemState(remove=[score_package]):
        input_ = 'new exampleScore1 q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()

    with abjad.FilesystemState(remove=[score_package]):
        input_ = 'new EXAMPLE_SCORE_1 q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()

    with abjad.FilesystemState(remove=[score_package]):
        input_ = 'new example_score_1 q'
        abjad_ide._start(input_=input_)
        assert score_package.exists()


def test_AbjadIDE_new_04():
    r'''Makes new build subdirectory.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'arch-a',
        )

    input_ = 'red~example~score bb new arch-a arch~a $80 ARCH-A y q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()


def test_AbjadIDE_new_05():
    r'''Coerces build subdirectory name.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'arch-a',
        )

    input_ = 'red~example~score bb new arch_a arch~a $80 ARCH-A y q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()


def test_AbjadIDE_new_06():
    r'''Makes new maker classfile.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'NewMaker.py',
        )

    input_ = 'red~example~score oo new NewMaker.py q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        with path.open() as file_pointer:
            string = file_pointer.read()
            assert 'class NewMaker(abjad.AbjadObject)' in string


def test_AbjadIDE_new_07():
    r'''Coerces maker classfile name.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'NewMaker.py',
        )

    input_ = 'red~example~score oo new New~Maker q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        with path.open() as file_pointer:
            string = file_pointer.read()
            assert 'class NewMaker(abjad.AbjadObject)' in string


def test_AbjadIDE_new_08():
    r'''Makes new maker functionfile.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'make_material.py',
        )

    input_ = 'red~example~score oo new make_material.py q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        with path.open() as file_pointer:
            string = file_pointer.read()
            assert 'def make_material():' in string


def test_AbjadIDE_new_09():
    r'''Coerces maker functionfile name.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'make_material.py',
        )

    input_ = 'red~example~score oo new make~material q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        with path.open() as file_pointer:
            string = file_pointer.read()
            assert 'def make_material():' in string


def test_AbjadIDE_new_10():
    r'''Makes new material directory.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'test_notes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'Red~Example~Score mm new test_notes q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_11():
    r'''Coerces material directory name.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'test_notes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'Red~Example~Score mm new test~notes q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_12():
    r'''Makes new segment directory.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'red~example~score gg new segment_04 q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_13():
    r'''Coerces segment directory name.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    input_ = 'red~example~score gg new segment~04 q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
        entries = list(path.glob('*'))
        for entry in directory_entries:
            assert path / entry in entries, repr(entry)


def test_AbjadIDE_new_14():
    r'''Makes new stylesheet.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'new-stylesheet.ily',
        )

    input_ = 'red~example~score yy new new-stylesheet.ily q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()


def test_AbjadIDE_new_15():
    r'''Coerces stylesheet new.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'new-stylesheet.ily',
        )

    input_ = 'red~example~score yy new new~stylesheet q'

    with abjad.FilesystemState(remove=[path]):
        abjad_ide._start(input_=input_)
        assert path.exists()
