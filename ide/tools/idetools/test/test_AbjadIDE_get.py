import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_get_01():
    r'''In build directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'builds', 'letter', 'front-cover.tex')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu %letter get red ont-co y q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : builds : letter'
        header += ' : get files from ...'
        assert header in transcript
        assert header in transcript
        header = 'Blue Score (2017) : distribution'
        header += ' : get Red Score (2017) files ...'
        assert f'> red' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_02():
    r'''In distribution directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'distribution', 'red-score.pdf')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu dd get red ore.pdf y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : distribution'
        header += ' : get files from ...'
        assert header in transcript
        header = 'Blue Score (2017) : distribution'
        header += ' : get Red Score (2017) files ...'
        assert header in transcript
        assert '> red' in transcript
        assert '> ore.pdf' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_03():
    r'''In etc directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'etc', 'notes.txt')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu ee get red otes.txt y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : etc : get files from ...'
        assert header in transcript
        header = 'Blue Score (2017) : etc'
        header += ' : get Red Score (2017) files ...'
        assert header in transcript
        assert '> red' in transcript
        assert '> otes.txt' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_04():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path('blue_score', 'materials', 'blue_rhythm_1')
        source /= 'definition.py'
        assert source.is_file()
        target = source.with_parent('blue_rhythm_2')
        target.remove()

        abjad_ide(f'blu mm br2 get br1 y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : materials : blue_rhythm_2 : get file ...'
        assert header in transcript
        for name in ['blue_rhythm_1', 'blue_rhythm_2']:
            path = source.materials(name, 'definition.py')
            assert path.trim() in transcript
        assert f'> br1' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_05():
    r'''In materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'materials', 'red_pitch_classes')
        assert source.is_dir()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu mm get red rpc y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : materials : get packages from ...'
        assert header in transcript
        assert '> red' in transcript
        assert '> rpc' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_06():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'segments', 'A', 'definition.py')
        assert source.is_file()
        target = source.with_parent('B')
        target.remove()

        abjad_ide(f'red %B get A y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Red Score (2017) : segments : B : get file ...'
        assert header in transcript
        assert f'> A' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript

    # regression: return jumps from selector
    abjad_ide(f'blu %_ get <return> q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Blue Score (2017)',
        'Blue Score (2017) : segments : _',
        'Blue Score (2017) : segments : _ : get file ...',
        'Blue Score (2017) : segments : _',
        ]

    # regression: quit jumps from selector
    abjad_ide(f'blu %_ get q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Blue Score (2017)',
        'Blue Score (2017) : segments : _',
        'Blue Score (2017) : segments : _ : get file ...',
        ]
    assert "Matches no file 'q' ..." not in transcript


def test_AbjadIDE_get_07():
    r'''In segments directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'segments', 'B')
        assert source.is_dir()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu gg get red B y <return> q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : segments : get packages from ...'
        assert header in transcript
        header = 'Blue Score (2017) : segments'
        header += ' : get Red Score (2017) packages ...'
        assert header in transcript
        assert '> red' in transcript
        assert '> B' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_08():
    r'''In stylesheets directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'stylesheets', 'stylesheet.ily')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu yy get red eet.i y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : stylesheets (empty) : get files from ...'
        assert header in transcript
        assert '> red' in transcript
        assert '> eet.i' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_09():
    r'''In test directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'test', 'test_materials.py')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu tt get red _mat y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : test (empty) : get files from ...'
        assert header in transcript
        assert '> red' in transcript
        assert '> _mat' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_10():
    r'''In tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score', 'tools', 'ScoreTemplate.py')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu oo get red ST y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : tools : get files from ...'
        assert header in transcript
        assert f'> red' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript
