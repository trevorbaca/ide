import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_new_01():
    r'''Makes new score directory.
    '''

    with ide.Test():
        package = ide.Path('example_scores') / 'green_score'
        contents = package / package.name
        package_names = [
            '.gitignore',
            '.travis.yml',
            'README.md',
            'green_score',
            'requirements.txt',
            'setup.cfg',
            'setup.py',
            ]
        contents_names = [
            '__init__.py',
            '__metadata__.py',
            'build',
            'distribution',
            'etc',
            'materials',
            'segments',
            'stylesheets',
            'test',
            'tools',
            ]
        materials_names = ['__init__.py']
        segments_names = ['__init__.py']

        input_ = 'new Green~Score q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert package.is_dir()
        for name in package_names:
            path = package / name
            assert path.exists()
        for name in contents_names:
            path = contents / name
            assert path.exists()
        for name in materials_names:
            path = contents.materials / name
            assert path.exists()
        for name in segments_names:
            path = contents.segments / name
            assert path.exists()
        assert 'Enter title]> Green Score' in transcript
        assert f'Making {package} ...' in transcript


def test_AbjadIDE_new_02():
    r'''Makes new score directory in preexisting empty directory.
    '''

    with ide.Test():
        package = ide.Path('example_scores') / 'green_score'
        contents = package / package.name
        package_names = [
            '.travis.yml',
            'README.md',
            'requirements.txt',
            'setup.cfg',
            'setup.py',
            ]
        contents_names = [
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
        materials_names = ['__init__.py']
        segments_names = ['__init__.py' ]
        git = package / '.git'
        package.remove()
        package.mkdir()
        git.mkdir()

        input_ = 'new y Green~Score q'
        assert package.is_dir()
        assert git.is_dir()
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert package.exists()
        for name in package_names:
            path = package / name
            assert path.exists()
        for name in contents_names:
            path = contents / name
            assert path.exists()
        for name in materials_names:
            path = contents.materials / name
            assert path.exists()
        for name in segments_names:
            path = contents.segments / name
            assert path.exists()
        assert f'Found {package}.' in transcript
        assert f'Populate {package}?' in transcript
        assert 'Enter title]> Green Score' in transcript


def test_AbjadIDE_new_03():
    r'''Coerces package name.
    '''

    package = ide.Path('example_scores') / 'green_score'

    with ide.Test(remove=[package]):
        input_ = 'new GreenScore q'
        abjad_ide._start(input_=input_)
        assert package.is_dir()

    with ide.Test(remove=[package]):
        input_ = 'new greenScore q'
        abjad_ide._start(input_=input_)
        assert package.is_dir()

    with ide.Test(remove=[package]):
        input_ = 'new Green_Score q'
        abjad_ide._start(input_=input_)
        assert package.is_dir()

    with ide.Test(remove=[package]):
        input_ = 'new green_score q'
        abjad_ide._start(input_=input_)
        assert package.is_dir()


def test_AbjadIDE_new_04():
    r'''Makes new build subdirectory.
    '''

    path = ide.Path('red_score').build / 'arch-a'
    with ide.Test(remove=[path]):
        input_ = 'red~score bb new arch-a arch~a $80 ARCH-A y q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()


def test_AbjadIDE_new_05():
    r'''Coerces build subdirectory name.
    '''

    path = ide.Path('red_score').build / 'arch-a'
    with ide.Test(remove=[path]):
        input_ = 'red~score bb new arch_a arch~a $80 ARCH-A y q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()


def test_AbjadIDE_new_06():
    r'''Makes new tools classfile.
    '''


    path = ide.Path('red_score').tools / 'NewClass.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new NewClass.py q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'class NewClass(abjad.AbjadObject)' in text


def test_AbjadIDE_new_07():
    r'''Coerces tools classfile name.
    '''

    path = ide.Path('red_score').tools / 'NewClass.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new New~Class q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'class NewClass(abjad.AbjadObject)' in text


def test_AbjadIDE_new_08():
    r'''Makes new tools functionfile.
    '''

    path = ide.Path('red_score').tools / 'make_material.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new make_material.py q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'def make_material():' in text


def test_AbjadIDE_new_09():
    r'''Coerces tools functionfile name.
    '''

    path = ide.Path('red_score').tools / 'make_material.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new make~material q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'def make_material():' in text


def test_AbjadIDE_new_10():
    r'''Makes new material directory.
    '''


    path = ide.Path('red_score').materials / 'test_notes'
    with ide.Test(remove=[path]):
        directory_names = [
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            ]

        input_ = 'Red~Score mm new test_notes q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()
        names = list(path.glob('*'))
        for name in directory_names:
            assert path / name in names, repr(name)


def test_AbjadIDE_new_11():
    r'''Coerces material directory name.
    '''

    path = ide.Path('red_score').materials / 'test_notes'
    with ide.Test(remove=[path]):
        directory_names = [
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            ]

        input_ = 'Red~Score mm new test~notes q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()
        names = list(path.glob('*'))
        for name in directory_names:
            assert path / name in names, repr(name)


def test_AbjadIDE_new_12():
    r'''Makes new segment directory.
    '''

    path = ide.Path('red_score').segments / 'segment_04'
    with ide.Test(remove=[path]):
        directory_names = [
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            ]

        input_ = 'red~score gg new segment_04 q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()
        names = list(path.glob('*'))
        for name in directory_names:
            assert path / name in names, repr(name)


def test_AbjadIDE_new_13():
    r'''Coerces segment directory name.
    '''

    path = ide.Path('red_score').segments / 'segment_04'
    with ide.Test(remove=[path]):
        directory_names = [
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            ]

        input_ = 'red~score gg new segment~04 q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()
        names = list(path.glob('*'))
        for name in directory_names:
            assert path / name in names, repr(name)


def test_AbjadIDE_new_14():
    r'''Makes new stylesheet.
    '''

    path = ide.Path('red_score').stylesheets / 'new-stylesheet.ily'
    with ide.Test(remove=[path]):
        input_ = 'red~score yy new new-stylesheet.ily q'
        abjad_ide._start(input_=input_)
        assert path.is_file()


def test_AbjadIDE_new_15():
    r'''Coerces stylesheet new.
    '''

    path = ide.Path('red_score').stylesheets / 'new-stylesheet.ily'
    with ide.Test(remove=[path]):
        input_ = 'red~score yy new new~stylesheet q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
