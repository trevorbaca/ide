import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_new_01():
    r'''Makes new score directory.
    '''

    with ide.Test():
        package = ide.PackagePath('test_scores') / 'green_score'
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
            'builds',
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
        transcript = abjad_ide._transcript
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
        package = ide.PackagePath('test_scores') / 'green_score'
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
            'builds',
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
        transcript = abjad_ide._transcript
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

    package = ide.PackagePath('test_scores') / 'green_score'

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


# TODO: add transcript tests
def test_AbjadIDE_new_04():
    r'''Makes new build directory.
    '''

    path = ide.PackagePath('red_score').builds / 'arch-a'
    with ide.Test(remove=[path]):
        input_ = 'red~score bb new arch-a arch~a $80 ARCH-A y q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()
        assert path.get_metadatum('price') == '$80'
        assert path.get_metadatum('catalog_number_suffix') == 'ARCH-A'


# TODO: add transcript tests
def test_AbjadIDE_new_05():
    r'''Makes new build directory. Ignores empty metadata.
    '''

    path = ide.PackagePath('red_score').builds / 'arch-a'
    with ide.Test(remove=[path]):
        input_ = 'red~score bb new arch-a arch~a <return> <return> y q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()
        assert path.get_metadatum('price') is None
        assert path.get_metadatum('catalog_number_suffix') is None


def test_AbjadIDE_new_06():
    r'''Coerces build directory name.
    '''

    path = ide.PackagePath('red_score').builds / 'arch-a'
    with ide.Test(remove=[path]):
        input_ = 'red~score bb new arch_a arch~a $80 ARCH-A y q'
        abjad_ide._start(input_=input_)
        assert path.is_dir()


def test_AbjadIDE_new_07():
    r'''Makes new tools classfile.
    '''

    path = ide.PackagePath('red_score').tools / 'NewClass.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new NewClass.py q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'class NewClass(abjad.AbjadObject)' in text


def test_AbjadIDE_new_08():
    r'''Coerces tools classfile name.
    '''

    path = ide.PackagePath('red_score').tools / 'NewClass.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new New~Class q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'class NewClass(abjad.AbjadObject)' in text


def test_AbjadIDE_new_09():
    r'''Makes new tools functionfile.
    '''

    path = ide.PackagePath('red_score').tools / 'make_material.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new make_material.py q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'def make_material():' in text


def test_AbjadIDE_new_10():
    r'''Coerces tools functionfile name.
    '''

    path = ide.PackagePath('red_score').tools / 'make_material.py'
    with ide.Test(remove=[path]):
        input_ = 'red~score oo new make~material q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        text = path.read_text()
        assert 'def make_material():' in text


def test_AbjadIDE_new_11():
    r'''Makes new material directory.
    '''

    path = ide.PackagePath('red_score').materials / 'test_notes'
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


def test_AbjadIDE_new_12():
    r'''Coerces material directory name.
    '''

    path = ide.PackagePath('red_score').materials / 'test_notes'
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


def test_AbjadIDE_new_13():
    r'''Makes new segment directory.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_04'
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


def test_AbjadIDE_new_14():
    r'''Coerces segment directory name.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_04'
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


def test_AbjadIDE_new_15():
    r'''Makes new stylesheet.
    '''

    path = ide.PackagePath('red_score').stylesheets / 'new-stylesheet.ily'
    with ide.Test(remove=[path]):
        input_ = 'red~score yy new new-stylesheet.ily q'
        abjad_ide._start(input_=input_)
        assert path.is_file()


def test_AbjadIDE_new_16():
    r'''Coerces stylesheet new.
    '''

    path = ide.PackagePath('red_score').stylesheets / 'new-stylesheet.ily'
    with ide.Test(remove=[path]):
        input_ = 'red~score yy new new~stylesheet q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
