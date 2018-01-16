import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_new_01():
    r'''Makes score package.
    '''

    with ide.Test():

        abjad_ide('new Green~Score q')
        transcript = abjad_ide.io.transcript
        wrapper = ide.Path('test_scores') / 'green_score'
        assert wrapper.is_dir()
        for name in [
            '.gitignore',
            '.travis.yml',
            'README.md',
            'green_score',
            'requirements.txt',
            'setup.cfg',
            'setup.py',
            ]:
            assert (wrapper / name).exists()
        for name in [
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
            ]:
            assert wrapper.contents(name).exists()
        assert wrapper.materials('__init__.py').is_file()
        assert wrapper.segments('__init__.py').is_file()
        assert 'Enter title> Green Score' in transcript
        assert f'Making {wrapper.trim()} ...' in transcript

        abjad_ide('new Green~Score q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {wrapper.trim()} ...' in transcript


def test_AbjadIDE_new_02():
    r'''Makes score package in empty directory.
    '''

    with ide.Test():
        wrapper = ide.Path('test_scores') / 'green_score'
        wrapper.remove()
        wrapper.mkdir()
        assert wrapper.is_dir()
        git = wrapper / '.git'
        git.mkdir()
        assert git.is_dir()

        abjad_ide('new y Green~Score q')
        transcript = abjad_ide.io.transcript
        assert wrapper.exists()
        for name in [
            '.travis.yml',
            'README.md',
            'requirements.txt',
            'setup.cfg',
            'setup.py',
            ]:
            assert (wrapper / name).exists()
        for name in [
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
            ]:
            assert wrapper.contents(name).exists()
        assert wrapper.materials('__init__.py').is_file()
        assert wrapper.segments('__init__.py').is_file()
        assert f'Found {wrapper.trim()}.' in transcript
        assert f'Populate {wrapper.trim()}?>' in transcript
        assert 'Enter title> Green Score' in transcript
        assert f'Making {wrapper.trim()} ...' in transcript

        abjad_ide('new Green~Score q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {wrapper.trim()} ...' in transcript


def test_AbjadIDE_new_03():
    r'''Coerces package name.
    '''

    package = ide.Path('test_scores') / 'green_score'

    with ide.Test(remove=[package]):

        abjad_ide('new GreenScore q')
        assert package.is_dir()

    with ide.Test(remove=[package]):

        abjad_ide('new greenScore q')
        assert package.is_dir()

    with ide.Test(remove=[package]):

        abjad_ide('new Green_Score q')
        assert package.is_dir()

    with ide.Test(remove=[package]):

        abjad_ide('new green_score q')
        assert package.is_dir()


def test_AbjadIDE_new_04():
    r'''Makes build directory.
    '''

    build = ide.Path('red_score', 'builds', 'arch-a-score')
    with ide.Test(remove=[build]):

        abjad_ide('red bb new arch-a-score arch~a $80 ARCH-A y q')
        transcript = abjad_ide.io.transcript
        assert build.is_dir()
        assert build.get_metadatum('price') == '$80'
        assert build.get_metadatum('catalog_number_suffix') == 'ARCH-A'
        assert 'Build name> arch-a-score' in transcript
        assert 'Paper size> arch a' in transcript
        assert r'Price> $80' in transcript
        assert 'Catalog number suffix> ARCH-A'in transcript
        assert transcript.lines[-34:] == [
            'Writing red_score/builds/arch-a-score/back-cover.tex ...',
            '',
            'Writing red_score/builds/arch-a-score/front-cover.tex ...',
            '',
            'Writing red_score/builds/arch-a-score/layout.py ...',
            '',
            'Collecting segment lys ...',
            'Writing red_score/builds/arch-a-score/_segments/segment-_.ly ...',
            'Writing red_score/builds/arch-a-score/_segments/segment-A.ly ...',
            'Writing red_score/builds/arch-a-score/_segments/segment-B.ly ...',
            'No + tags to deactivate ...',
            'No -ARCH_A_SCORE tags to deactivate ...',
            'No +ARCH_A_SCORE tags to activate ...',
            'No SPACING tags to activate ...',
            'No persistent indicator tags to deactivate ...',
            'No persistent indicator tags to activate ...',
            'No markup tags to deactivate ...',
            '',
            'Examining segments alphabetically ...',
            'Examining red_score/segments/_ ...',
            'Examining red_score/segments/A ...',
            'Examining red_score/segments/B ...',
            'Writing red_score/builds/arch-a-score/music.ly ...',
            '',
            'Writing red_score/builds/arch-a-score/preface.tex ...',
            '',
            'Generating score ...',
            'Writing red_score/builds/arch-a-score/score.tex ...',
            '',
            'Generating stylesheet ...',
            'Writing red_score/builds/arch-a-score/stylesheet.ily ...',
            '',
            '> q',
            '',
            ]

        abjad_ide('red bb new arch-a-score q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {build.trim()} ...' in transcript


def test_AbjadIDE_new_05():
    r'''Makes build directory. Ignores empty metadata.
    '''

    path = ide.Path('red_score', 'builds', 'arch-a-score')
    with ide.Test(remove=[path]):

        abjad_ide('red bb new arch-a-score arch~a <return> <return> y q')
        transcript = abjad_ide.io.transcript
        assert path.is_dir()
        assert path.get_metadatum('price') is None
        assert path.get_metadatum('catalog_number_suffix') is None
        assert 'Build name> arch-a-score' in transcript
        assert 'Paper size> arch a' in transcript
        assert r'Price>' in transcript
        assert 'Catalog number suffix>'in transcript
        assert 'Making ...' in transcript
        assert f'    {path.trim()}' in transcript
        paths = [path / _ for _ in (
            'back-cover.tex',
            'front-cover.tex',
            'music.ly',
            'preface.tex',
            'score.tex',
            'stylesheet.ily',
            )]
        for path in paths:
            assert f'    {path.trim()}' in transcript
        assert 'Ok?> y' in transcript
        assert 'Generating score ...' in transcript
        assert 'Generating stylesheet ...' in transcript
        for path in paths:
            assert f'Writing {path.trim()} ...' in transcript


def test_AbjadIDE_new_06():
    r'''Makes tools classfile.
    '''

    path = ide.Path('red_score', 'tools', 'NewClass.py')
    with ide.Test(remove=[path]):

        abjad_ide('red oo new NewClass.py y q')
        transcript = abjad_ide.io.transcript
        assert path.is_file()
        text = path.read_text()
        assert 'class NewClass(abjad.AbjadObject)' in text
        assert 'File name> NewClass' in transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert 'Ok?> y' in transcript

        abjad_ide('red oo new NewClass q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...'


def test_AbjadIDE_new_07():
    r'''Makes tools functionfile.
    '''

    path = ide.Path('red_score', 'tools', 'make_material.py')
    with ide.Test(remove=[path]):

        abjad_ide('red oo new make_material y q')
        transcript = abjad_ide.io.transcript
        assert path.is_file()
        text = path.read_text()
        assert 'def make_material():' in text
        assert 'File name> make_material' in transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert 'Ok?> y' in transcript

        abjad_ide('red oo new make~material q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...'


def test_AbjadIDE_new_08():
    r'''Makes material directory.
    '''

    path = ide.Path('red_score', 'materials', 'test_notes')
    with ide.Test(remove=[path]):

        abjad_ide('red mm new test~notes q')
        transcript = abjad_ide.io.transcript
        assert path.is_dir()
        names = [
            '__init__.py',
            'definition.py',
            ]
        for name in names:
            assert (path / name).is_file()
        assert 'Enter package name> test notes' in transcript
        assert f'Making {path.trim()} ...' in transcript
        for name in names:
            assert f'Writing {(path / name).trim()} ...' in transcript

        abjad_ide('red mm new test_notes q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...'


def test_AbjadIDE_new_09():
    r'''Makes segment directory.
    '''

    path = ide.Path('red_score', 'segments', 'segment_04')
    with ide.Test(remove=[path]):

        abjad_ide('red gg new segment~04 q')
        transcript = abjad_ide.io.transcript
        assert path.is_dir()
        names = [
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            ]
        for name in names:
            assert (path / name).is_file()
        assert 'Enter package name> segment 04' in transcript
        assert f'Making {path.trim()} ...' in transcript
        for name in names:
            assert f'Writing {(path / name).trim()} ...' in transcript

        abjad_ide('red gg new segment_04 q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...'


def test_AbjadIDE_new_10():
    r'''Makes stylesheet.
    '''

    path = ide.Path('red_score', 'stylesheets', 'new-stylesheet.ily')
    with ide.Test(remove=[path]):

        abjad_ide('red yy new new~stylesheet y q')
        transcript = abjad_ide.io.transcript
        assert path.is_file()
        assert 'File name> new stylesheet' in transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert 'Ok?> y' in transcript

        abjad_ide('red yy new new~stylesheet.ily q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...'

        abjad_ide('red yy new <return> q')
        transcript = abjad_ide.io.transcript
        assert 'Existing' not in transcript
        assert 'Writing' not in transcript

        abjad_ide('red yy new ss q')
        transcript = abjad_ide.io.transcript
        assert 'Existing' not in transcript
        assert 'Writing' not in transcript


def test_AbjadIDE_new_11():
    r'''In library.
    '''

    if not abjad.abjad_configuration.composer_library_tools:
        return

    directory = ide.Path(abjad.abjad_configuration.composer_library_tools)
    with abjad.FilesystemState(keep=[directory]):

        abjad_ide('ll new FooCommand y q')
        transcript = abjad_ide.io.transcript
        path = directory / 'FooCommand.py'
        assert path.is_file()
        assert 'File name> FooCommand' in transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert 'Ok?> y' in transcript

        abjad_ide('ll new FooCommand q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...' in transcript

        abjad_ide('ll new foo~command y q')
        transcript = abjad_ide.io.transcript
        path = directory / 'foo_command.py'
        assert path.is_file()
        assert 'File name> foo command' in transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert 'Ok?> y' in transcript

        abjad_ide('ll new foo~command q')
        transcript = abjad_ide.io.transcript
        assert f'Existing {path.trim()} ...' in transcript
