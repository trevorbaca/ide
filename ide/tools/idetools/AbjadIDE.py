import abjad
import datetime
import importlib
import inspect
import os
import pathlib
import platform
import shutil
from ide.tools.idetools.Command import Command
from ide.tools.idetools.Configuration import Configuration
from ide.tools.idetools.Interaction import Interaction
from ide.tools.idetools.IOManager import IOManager
from ide.tools.idetools.Menu import Menu
from ide.tools.idetools.MenuSection import MenuSection
from ide.tools.idetools.Path import Path


class AbjadIDE(abjad.AbjadObject):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> ide.AbjadIDE(terminal_dimensions=(24, 80))
            AbjadIDE(terminal_dimensions=(24, 80))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_aliases',
        '_clipboard',
        '_commands',
        '_current_directory',
        '_io',
        '_is_example',
        '_is_test',
        '_navigation',
        '_navigations',
        '_previous_directory',
        '_terminal_dimensions',
        )

    # taken from:
    # http://lilypond.org/doc/v2.19/Documentation/notation/predefined-paper-sizes
    _paper_size_to_paper_dimensions = {
        'a3': '297 x 420 mm',
        'a4': '210 x 297 mm',
        'arch a': '9 x 12 in',
        'arch b': '12 x 18 in',
        'arch c': '18 x 24 in',
        'arch d': '24 x 36 in',
        'arch e': '36 x 48 in',
        'legal': '8.5 x 14 in',
        'ledger': '17 x 11 in',
        'letter': '8.5 x 11 in',
        'tabloid': '11 x 17 in',
        }

    configuration = Configuration()

    ### INITIALIZER ###

    def __init__(
        self,
        is_example=None,
        is_test=None,
        terminal_dimensions=None,
        ):
        self._aliases = dict(self.configuration.aliases)
        self._clipboard = []
        self._current_directory = None
        self._is_example = is_example
        self._is_test = is_test
        self._navigation = None
        self._previous_directory = None
        if terminal_dimensions is None and not is_test:
            terminal_dimensions = self._get_terminal_dimensions()
        self._terminal_dimensions = terminal_dimensions
        self._io = IOManager(terminal_dimensions=terminal_dimensions)
        self._check_test_scores_directory(is_example or is_test)
        self._cache_commands()

    ### SPECIAL METHODS ###

    def __call__(self, string=None):
        r'''Calls IDE on `string`.

        Returns none.
        '''
        if self.is_test and not string.endswith('q'):
            raise Exception(f"Test input must end with 'q': {string!r}.")
        self.__init__(
            is_example=self.is_example,
            is_test=self.is_test,
            terminal_dimensions=self.terminal_dimensions,
            )
        self.io.pending_input(string)
        scores = self._get_scores_directory()
        self._manage_directory(scores)
        last_line = self.io.transcript.lines[-1]
        assert last_line == '', repr(last_line)
        self.io.clear_terminal()

    ### PRIVATE METHODS ###

    def _cache_commands(self):
        commands = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            try:
                command = getattr(self, name)
            except AttributeError:
                command = None
            if not inspect.ismethod(command):
                continue
            if not hasattr(command, 'command_name'):
                continue
            commands[command.command_name] = command
        self._commands = commands

    def _check_test_scores_directory(self, check=False):
        if not check:
            return
        directory = self.configuration.test_scores_directory
        names = [_.name for _ in directory.iterdir()]
        if 'red_score' not in names:
            message = f'Empty test scores directory {directory} ...'
            raise Exception(message)

    def _copy_boilerplate(
        self,
        directory,
        source_name,
        target_name=None,
        values=None,
        ):
        target_name = target_name or source_name
        target = directory / target_name
        if target.exists():
            self.io.display(f'removing {target.trim()} ...')
        self.io.display(f'writing {target.trim()} ...')
        directory.copy_boilerplate(
            source_name=source_name,
            target_name=target_name,
            values=values,
            )

    def _get_library(self):
        name = abjad.abjad_configuration.composer_library
        if not name:
            return
        try:
            path = importlib.import_module(name)
        except ImportError:
            path = None
        if not path:
            return
        path = Path(path.__path__[0]) / 'tools'
        return path

    def _get_score_names(self):
        scores = self._get_scores_directory()
        names = [_.name for _ in scores.list_paths()]
        return names

    def _get_scores_directory(self):
        if (self.is_test or self.is_example):
            return self.configuration.test_scores_directory
        return self.configuration.composer_scores_directory

    def _get_terminal_dimensions(self):
        result = os.popen('stty size', 'r').read().split()
        if result:
            height, width = result
            height = int(height)
            width = int(width)
        else:
            height, width = 24, 80
        return height, width

    def _interpret_tex_file(self, tex):
        if not tex.is_file():
            self.io.display(f'can not find {tex.trim()} ...')
            return
        pdf = tex.with_suffix('.pdf')
        if pdf.exists():
            self.io.display(f'removing {pdf.trim()} ...')
            pdf.unlink()
        self.io.display(f'interpreting {tex.trim()} ...')
        self.io.interpret_tex_file(tex)
        if pdf.is_file():
            self.io.display(f'writing {pdf.trim()} ...')
        else:
            self.io.display('ERROR IN LATEX LOG FILE ...')
            log_file = self.configuration.latex_log_file_path
            with log_file.open() as file_pointer:
                lines = [_.strip('\n') for _ in file_pointer.readlines()]
            self.io.display(lines)

    def _make_build_directory(self, builds):
        name = self.io.get('build name')
        if self.is_navigation(name):
            return
        name = builds.coerce_asset_name(name)
        build = builds / name
        if build.exists():
            self.io.display(f'existing {build.trim()} ...')
            return
        paper_size = self.io.get('paper size (ex: letter landscape)')
        if self.is_navigation(paper_size):
            return
        orientation = 'portrait'
        if paper_size.endswith(' landscape'):
            orientation = 'landscape'
            length = len(' landscape')
            paper_size = paper_size[:-length]
        elif paper_size.endswith(' portrait'):
            length = len(' portrait')
            paper_size = paper_size[:-length]
        price = self.io.get('price (ex: \$80 / \euro 72)')
        suffix = self.io.get('catalog number suffix (ex: ann.)')
        names = (
            'back-cover.tex',
            'front-cover.tex',
            'music.ly',
            'preface.tex',
            'score.tex',
            'stylesheet.ily',
            )
        paths = [build / _ for _ in names]
        self.io.display('making ...')
        self.io.display(f'    {build.trim()}')
        for path in paths:
            self.io.display(f'    {path.trim()}')
        if not self.io.confirm():
            return
        assert not build.exists()
        build.mkdir()
        if bool(paper_size):
            build.add_metadatum('paper_size', paper_size)
        if not orientation == 'portrait':
            build.add_metadatum('orientation', orientation)
        if bool(price):
            build.add_metadatum('price', price)
        if bool(suffix):
            build.add_metadatum('catalog_number_suffix', suffix)
        self.generate_back_cover(build)
        self.generate_front_cover(build)
        self.generate_music(build)
        self.generate_preface(build)
        self.generate_score(build)
        self.generate_build_stylesheet(build)

    def _make_command_sections(self, directory):
        commands = []
        for command in self.commands.values():
            if directory.is_external() and command.external:
                commands.append(command)
            elif directory.is_scores() and command.scores:
                commands.append(command)
            elif (directory.is_package_path() and
                directory.matches_manifest(command.directories) and
                not directory.matches_manifest(command.blacklist)):
                commands.append(command)
        entries_by_section = {}
        navigations = {}
        navigation_sections = ('back-home-quit', 'navigation', 'scores')
        for command in commands:
            if command.section not in entries_by_section:
                entries_by_section[command.section] = []
            entries = entries_by_section[command.section]
            display = f'{command.description} ({command.command_name})'
            entry = (display, command.command_name)
            entries.append(entry)
            if command.section in navigation_sections:
                name = command.command_name
                navigations[name] = command
        self._navigations = navigations
        sections = []
        for name in entries_by_section:
            entries = entries_by_section[name]
            section = MenuSection(
                command=name,
                entries=entries,
                )
            sections.append(section)
        return sections

    def _make_file(self, directory):
        assert directory.is_dir()
        name = self.io.get('file name')
        if self.is_navigation(name):
            return
        if directory.is_package_path():
            name = directory.coerce_asset_name(name)
            predicate = directory.get_name_predicate()
            if predicate and not predicate(abjad.String(name)):
                self.io.display(f'invalid file name {name!r} ...')
                return
        elif directory == self._get_library():
            suffix = Path(name).suffix
            if suffix and suffix != '.py':
                self.io.display(f'invalid file name {name!r} ...')
            stem = abjad.String(Path(name).stem)
            if stem.islower():
                stem = stem.to_snake_case()
            else:
                stem = stem.to_upper_camel_case()
            suffix = suffix or '.py'
            name = stem + suffix
        target = directory / name
        boilerplate = self.configuration.boilerplate_directory
        if target.exists():
            self.io.display(f'existing {target.trim()} ...')
            return
        else:
            self.io.display(f'writing {target.trim()} ...')
            if not self.io.confirm():
                return
        if directory.is_tools():
            if abjad.String(name).is_classfile_name():
                source = boilerplate / 'Maker.py'
                shutil.copyfile(str(source), str(target))
                template = target.read_text()
                template = template.format(class_name=target.stem)
                target.write_text(template)
            else:
                source = boilerplate / 'make_something.py'
                shutil.copyfile(str(source), str(target))
                template = target.read_text()
                template = template.format(function_name=target.stem)
                target.write_text(template)
        else:
            self.io.write(target, '')

    def _make_material_ly(self, directory):
        assert directory.is_dir()
        directory = Path(directory)
        assert directory.parent.name == 'materials'
        definition = directory / 'definition.py'
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return
        source = directory / '__illustrate__.py'
        if not source.is_file():
            self.io.display(f'can not find {source.trim()} ...')
            return
        target = directory / 'illustration.ly'
        if target.exists():
            self.io.display(f'removing {target.trim()} ...')
        source_make = Path('boilerplate')
        source_make /= '__make_material_ly__.py'
        target_make = directory / '__make_material_ly__.py'
        with self.io.cleanup([target_make]):
            target_make.remove()
            shutil.copyfile(str(source_make), str(target_make))
            self.io.display(f'interpreting {source.trim()} ...')
            result = self.io.interpret_file(str(target_make))
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.io.display_errors(stderr_lines)
                return
            if not target.is_file():
                self.io.display(f'could not make {target.trim()}.')
                return
            self.io.display(f'writing {target.trim()} ...')

    def _make_material_pdf(self, directory, open_after=True):
        assert directory.is_material()
        illustrate = directory / '__illustrate__.py'
        if not illustrate.is_file():
            self.io.display(f'can not find {illustrate.trim()} ...')
            return 0 
        definition = directory / 'definition.py'
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return 0 
        self.io.display('making PDF ...')
        source = directory / 'illustration.ly'
        target = source.with_suffix('.pdf')
        boilerplate = Path('boilerplate')
        source_make = boilerplate / '__make_material_pdf__.py'
        target_make = directory / '__make_material_pdf__.py'
        with self.io.cleanup([target_make]):
            for path in (source, target):
                if path.exists():
                    self.io.display(f'removing {path.trim()} ...')
                    path.remove()
            shutil.copyfile(str(source_make), str(target_make))
            self.io.display(f'interpreting {illustrate.trim()} ...')
            result = self.io.interpret_file(target_make)
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.io.display_errors(stderr_lines)
            if open_after:
                self.io.display(f'opening {target.trim()} ...')
                self.___open_file(str(target))
            return exit_code

    def _make_package(self, directory):
        assert directory.is_dir()
        asset_type = directory.get_asset_type()
        name = self.io.get(f'enter {asset_type} name')
        if self.is_navigation(name):
            return
        name = directory.coerce_asset_name(name)
        path = directory / name
        if path.exists():
            self.io.display(f'existing {path.trim()} ...')
            return
        self.io.display(f'making {path.trim()} ...')
        path.mkdir()
        for name in ('__init__.py', '__metadata__.py', 'definition.py'):
            boilerplate = abjad.abjad_configuration.boilerplate_directory
            boilerplate = Path(boilerplate)
            if name == '__init__.py':
                source = boilerplate / 'empty.py'
            else:
                source = boilerplate / name
            target = path / name
            self.io.display(f'writing {target.trim()} ...')
            shutil.copyfile(str(source), str(target))
        paths = path.parent.list_paths()
        if path not in paths:
            view = path.parent.get_metadatum('view')
            if view is not None:
                path.parent.add_metadatum('_view', view) 
                path.parent.remove_metadatum('view')

    def _make_score_package(self):
        scores = self._get_scores_directory()
        wrapper = scores._find_empty_wrapper()
        if wrapper is not None:
            self.io.display(f'found {wrapper}.')
            if not self.io.confirm(f'populate {wrapper}?'):
                return
        title = self.io.get('enter title')
        if self.is_navigation(title):
            return
        if wrapper is None:
            name = scores.coerce_asset_name(title)
            wrapper = scores / name
            if wrapper.exists():
                self.io.display(f'existing {wrapper} ...')
                return
        self.io.display(f'making {wrapper} ...')
        year = datetime.date.today().year
        abjad.IOManager._make_score_package(
            score_package_path=str(wrapper),
            composer_email=abjad.abjad_configuration.composer_email,
            composer_full_name=abjad.abjad_configuration.composer_full_name,
            composer_github_username=abjad.abjad_configuration.composer_github_username,
            composer_last_name=abjad.abjad_configuration.composer_last_name,
            composer_library=abjad.abjad_configuration.composer_library,
            score_title=title,
            year=year,
            )
        for path in wrapper.builds.iterdir():
            if path.name == '.gitignore':
                continue
            path.remove()
        view = scores.get_metadatum('view', None)
        if view is not None:
            scores.add_metadatum('_view', view)
        scores.remove_metadatum('view')

    def _make_segment_ly(self, directory):
        assert directory.is_segment()
        definition = directory / 'definition.py'
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return
        directory.update_order_dependent_segment_metadata()
        boilerplate = self.configuration.boilerplate_directory
        source_make = boilerplate / '__make_segment_ly__.py'
        target_make = directory / '__make_segment_ly__.py'
        target_make.remove()
        with self.io.cleanup([target_make]):
            source = directory / '__illustrate__.py'
            target = directory / 'illustration.ly'
            if target.exists():
                self.io.display(f'removing {target.trim()} ...')
            shutil.copyfile(str(source_make), str(target_make))
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = 'previous_metadata = None'
            else:
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_metadata'
                statement = statement.format(
                    diretory.contents.name,
                    previous_segment.name,
                    )
            template = target_make.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            target_make.write_text(template)
            source = directory / '__illustrate__.py'
            if source.exists():
                self.io.display(f'removing {source.trim()} ...')
                self.io.display(f'writing {source.trim()} ...')
            self.io.display(f'interpreting {source.trim()} ...')
            result = self.io.interpret_file(target_make)
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.io.display_errors(stderr_lines)
                return
            self.io.display(f'writing {target.trim()} ...')

    def _make_segment_midi(self, directory, open_after=True):
        assert directory.is_segment()
        definition_path = directory / 'definition.py'
        if not definition_path.is_file():
            self.io.display(f'can not find {definition_path.trim()} ...')
            return -1
        self.io.display('making MIDI ...')
        directory.update_order_dependent_segment_metadata()
        boilerplate = self.configuration.boilerplate_directory
        boilerplate /= '__make_segment_midi__.py'
        maker = directory / '__midi__.py'
        ly = directory / 'midi.ly'
        midi = directory / 'segment.midi'
        for path in (ly, midi):
            if path.exists():
                self.io.display(f'removing {path.trim()} ...')
                path.unlink()
        if maker.exists():
            self.io.display(f'removing {maker.trim()} ...')
            maker.unlink()
        self.io.display(f'writing {maker.trim()} ...')
        self.io.display(f'interpreting {maker.trim()} ...')
        shutil.copyfile(str(boilerplate), str(maker))
        previous_segment = directory.get_previous_package()
        if previous_segment is None:
            statement = 'previous_metadata = None'
        else:
            statement = 'from {}.segments.{}.__metadata__'
            statement += ' import metadata as previous_metadata'
            statement = statement.format(
                directory.contents.name,
                previous_segment.name,
                )
        template = maker.read_text()
        template = template.format(
            previous_segment_metadata_import_statement=statement
            )
        maker.write_text(template)
        result = self.io.interpret_file(maker)
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display_errors(stderr_lines)
            return exit_code
        log = abjad.abjad_configuration.lilypond_log_file_path
        log = Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                self.io.display('ERROR IN LILYPOND LOG FILE ...')
                break
        if midi.is_file() and open_after:
            self._open_file(midi)
        return 0

    def _make_segment_pdf(self, directory, open_after=True):
        assert directory.is_segment()
        definition_path = directory / 'definition.py'
        if not definition_path.is_file():
            self.io.display(f'can not find {definition_path.trim()} ...')
            return -1
        self.io.display('making PDF ...')
        directory.update_order_dependent_segment_metadata()
        boilerplate = self.configuration.boilerplate_directory
        boilerplate_path = boilerplate / '__illustrate_segment__.py'
        illustrate = directory / '__illustrate__.py'
        ly = directory / 'illustration.ly'
        pdf = directory / 'illustration.pdf'
        for path in (ly, pdf):
            if path.exists():
                self.io.display(f'removing {path.trim()} ...')
                path.unlink()
        if illustrate.exists():
            self.io.display(f'removing {illustrate.trim()} ...')
            illustrate.unlink()
        self.io.display(f'writing {illustrate.trim()} ...')
        self.io.display(f'interpreting {illustrate.trim()} ...')
        shutil.copyfile(str(boilerplate_path), str(illustrate))
        previous_segment = directory.get_previous_package()
        if previous_segment is None:
            statement = 'previous_metadata = None'
        else:
            statement = 'from {}.segments.{}.__metadata__'
            statement += ' import metadata as previous_metadata'
            statement = statement.format(
                directory.contents.name,
                previous_segment.name,
                )
        template = illustrate.read_text()
        completed_template = template.format(
            previous_segment_metadata_import_statement=statement
            )
        illustrate.write_text(completed_template)
        result = self.io.interpret_file(illustrate)
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display_errors(stderr_lines)
            return exit_code
        log = abjad.abjad_configuration.lilypond_log_file_path
        log = Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                self.io.display('ERROR IN LILYPOND LOG FILE ...')
                break
        if pdf.is_file() and open_after:
            self._open_file(pdf)
        return 0

    def _make_selector(
        self,
        aliases=None,
        navigations=None,
        force_single_column=False,
        header=None,
        items=None,
        multiple=False,
        prompt=None,
        ):
        entries = []
        for item in items:
            if isinstance(item, tuple):
                assert len(item) == 2, repr(item)
                entry = item
            elif isinstance(item, str):
                entry = (item, item)
            else:
                raise TypeError(item)
            entries.append(entry)
        if not entries:
            sections = []
        else:
            section = MenuSection(
                entries=entries,
                force_single_column=force_single_column,
                multiple=multiple,
                )
            sections = [section]
        menu = Menu(
            aliases=aliases,
            navigations=navigations,
            getter=True,
            header=header,
            io=self.io,
            prompt=prompt,
            sections=sections,
            )
        return menu

    def _manage_directory(self, directory, redraw=True):
        if not directory.exists():
            self.io.display(f'missing {directory.trim()} ...')
            return
        assert directory.is_dir(), repr(directory)
        if not self.current_directory == directory:
            self._previous_directory = self.current_directory
            self._current_directory = directory
        sections = self._make_command_sections(directory)
        menu = Menu.from_directory(
            directory,
            aliases=self.aliases,
            io=self.io,
            navigations=self.navigations,
            sections=sections,
            )
        response = menu(redraw=redraw)
        if self.is_navigation(response.string):
            pass
        elif response.string.startswith('!'):
            with self.io.change(directory):
                self.io.invoke_shell(response.string[1:])
        elif response.string[0] in Path.address_characters:
            if isinstance(response.payload, Path):
                path = response.payload
            elif self.aliases and response.string[1:] in self.aliases:
                path = Path(self.aliases[response.string[1:]])
            else:
                path = directory.match_package_path(response.string)
            if path is None:
                if response.string[0] == '@':
                    message = 'matches no file {!r} ...'
                elif response.string[0] == '%':
                    message = 'matches no directory {!r} ...'
                elif response.string[0] == '^':
                    message = 'matches no Python file {!r} ...'
                elif response.string[0] == '*':
                    message = 'matches no PDF {!r} ...'
                else:
                    raise ValueError(response.string[0])
                message = message.format(response.string)
                self.io.display(message)
            elif response.string[0] == '@':
                if path.is_package():
                    path = path / 'definition.py'
                self._open_file(path)
            elif response.string[0] == '%':
                if path.is_wrapper():
                    path = path.contents
                self._manage_directory(path)
            elif response.string[0] == '^':
                self._run_doctest(path)
            elif response.string[0] == '*':
                if path.is_package():
                    path /= 'illustration.pdf'
                self._open_file(path)
        elif response.payload in self.commands:
            command = self.commands[response.payload]
            if command.argument_name == 'directory':
                command(self.current_directory)
            else:
                command()
        elif (isinstance(response.payload, Path) or
            self._match_alias(directory, response.string) is not None):
            if response.payload is None:
                path = self._match_alias(directory, response.string)
            else:
                path = response.payload
            if not path.exists() and path.suffix:
                self._open_file(path, allow_missing=True)
            elif path.is_file():
                self._open_file(path)
            elif path.is_dir():
                if path.is_wrapper():
                    path = path.contents
                self._manage_directory(path)
            else:
                self.io.display(f'missing {path.trim()} ...')
        else:
            assert response.payload is None, repr(response)
            self.io.display(f'unknown command {response.string!r} ...')
            if self.is_test:
                raise Exception(response)
        self.io.display('')
        if response.string == 'q':
            return
        elif self.navigation is not None:
            string = self.navigation
            self._navigation = None
            if string in self.commands:
                command = self.commands[string]
                if command.argument_name == 'directory':
                    command(self.current_directory)
                else:
                    command()
        else:
            redraw = response.string is None
            self._manage_directory(self.current_directory, redraw=redraw)

    def _match_alias(self, directory, string):
        if not self.aliases:
            return
        if not self.aliases.get(string):
            return
        value = self.aliases.get(string)
        path = Path(value)
        if path.exists():
            return path
        if (directory.is_package_path() and not directory.is_scores()):
            score_directory = directory.contents
            return directory.contents / value

    def _match_path(self, paths, argument):
        if abjad.mathtools.is_integer_equivalent(argument):
            argument = int(argument)
        if isinstance(argument, int):
            return paths[argument - 1]
        assert isinstance(argument, str), repr(argument)
        strings = [abjad.String(_.get_identifier()) for _ in paths]
        string = Path.smart_match(strings, argument)
        if string is not None:
            return paths[strings.index(string)]

    def _open_every_file(self, paths):
        for path in paths:
            if path.suffix in self.configuration.editor_suffixes:
                self.io.display(f'editing {path.trim()} ...')
            else:
                self.io.display(f'opening {path.trim()} ...')
        self.___open_file(paths)

    def _open_file(self, file_path):
        if file_path.is_file():
            if file_path.suffix in self.configuration.editor_suffixes:
                self.io.display(f'editing {file_path.trim()} ...')
            else:
                self.io.display(f'opening {file_path.trim()} ...')
            if not self.is_test:
                self.___open_file(file_path)
        else:
            self.io.display(f'missing {file_path.trim()} ...')

    def ___open_file(self, path, line_number=None):
        line_number_string = ''
        if line_number is not None:
            line_number_string = f' +{line_number}'
        if isinstance(path, str):
            path = pathlib.Path(path)
        if isinstance(path, list):
            path = [pathlib.Path(_) for _ in path]
        if not isinstance(path, list) and not path.is_file():
            pass
        if (isinstance(path, list) and
            all(_.suffix in self.configuration.editor_suffixes for _ in path)):
            paths = ' '.join([str(_) for _ in path])
            command = f'vim {paths}'
        elif isinstance(path, list):
            paths = path
            paths = ' '.join([str(_) for _ in paths])
            command = f'open {paths}'
        elif (path.name[0] == '.' or
            path.suffix in self.configuration.editor_suffixes):
            command = f'vim {path}'
        else:
            command = f'open {path}'
        command = command + line_number_string
        if self.is_test:
            return
        if isinstance(path, list):
            path_suffix = path[0].suffix
        else:
            path_suffix = path.suffix
        if (platform.system() == 'Darwin' and path_suffix == '.pdf'):
            source_path = pathlib.Path(
                self.configuration.boilerplate_directory,
                '__close_preview_pdf__.scr',
                )
            template = source_path.read_text()
            completed_template = template.format(file_path=path)
            script_path = pathlib.Path(
                self.configuration.home_directory,
                '__close_preview_pdf__.scr',
                )
            if script_path.exists():
                script_path.unlink()
            with abjad.FilesystemState(remove=[script_path]):
                script_path.write_text(completed_template)
                permissions_command = f'chmod 755 {script_path}'
                self.io.spawn_subprocess(permissions_command)
                close_command = str(script_path)
                self.io.spawn_subprocess(close_command)
        self.io.spawn_subprocess(command)

    @staticmethod
    def _replace_in_file(file_path, old, new):
        assert file_path.is_file()
        assert isinstance(old, str), repr(old)
        assert isinstance(new, str), repr(new)
        with file_path.open() as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        new_file_contents = ''.join(new_file_lines)
        file_path.write_text(new_file_contents)

    def _replace_in_tree(
        self,
        directory,
        search_string,
        replace_string,
        complete_words=False,
        ):
        command = f'ajv replace {search_string!r} {replace_string!r} -Y'
        if complete_words:
            command += ' -W'
        with self.io.change(directory):
            lines = self.io.run_command(command)
            lines = [_.strip() for _ in lines if not _ == '']
            return lines

    def _run_doctest(self, path):
        assert path.exists()
        self.io.display(f'running doctest on {path.trim()} ...')
        command = f'ajv doctest -x {path}'
        self.io.spawn_subprocess(command)

    def _run_lilypond(self, ly):
        assert ly.exists()
        if not abjad.IOManager.find_executable('lilypond'):
            message = 'cannot find LilyPond executable.'
            raise ValueError(message)
        directory = ly.parent
        pdf = ly.with_suffix('.pdf')
        backup_pdf = ly.with_suffix('._backup.pdf')
        if backup_pdf.exists():
            backup_pdf.unlink()
        with self.io.change(directory), self.io.cleanup([backup_pdf]):
            if pdf.exists():
                self.io.display(f'removing {pdf.trim()} ...')
                shutil.move(str(pdf), str(backup_pdf))
                assert not pdf.exists()
            else:
                backup_pdf = None
            self.io.display(f'interpreting {ly.trim()} ...')
            abjad.IOManager.run_lilypond(str(ly))
            if not pdf.is_file():
                self.io.display(f'can not produce {pdf.trim()} ...')
                if backup_pdf:
                    self.io.display(f'restoring {backup_pdf.trim()} ...')
                    shutil.move(str(backup_pdf), str(pdf))
            self.io.display(f'writing {pdf.trim()} ...')

    def _run_pytest(self, path):
        assert path.exists()
        self.io.display(f'running pytest on {path.trim()} ...')
        command = f'py.test -xrf {path}'
        self.io.spawn_subprocess(command)

    def _select_path(
        self,
        directory,
        infinitive='',
        multiple=False,
        scores=False,
        ):
        assert scores in (True, False) or isinstance(scores, str)
        paths = []
        local_contents = directory.list_paths()
        if directory.is_external() or directory.is_scores():
            paths.extend(local_contents)
        else:
            assert directory.is_package_path()
            paths = []
            if isinstance(scores, str) or not local_contents:
                for directory_ in directory.collect_cousins():
                    for path in directory_.list_paths():
                        if scores is True:
                            paths.append(path)
                        elif path.wrapper.name == scores:
                            paths.append(path)
            else:
                paths.extend(local_contents)
        asset_type = directory.get_asset_type()
        asset_types = abjad.String(asset_type).pluralize()
        if not paths:
            self.io.display(f'missing {directory.name} {asset_types} ...')
            return
        if multiple:
            asset_type = asset_types
        if infinitive:
            infinitive_ = ' ' + infinitive
        else:
            infinitive_ = infinitive
        items = []
        if (directory.is_external() or
            directory.is_scores() or
            (local_contents and not isinstance(scores, str))):
            header = None
            for path in paths:
                items.append((path.get_identifier(), path))
            prompt = f'select {asset_type}{infinitive_}'
            redraw = False
        else:
            header = directory.get_header()
            header = f'{header} - select {asset_type}{infinitive_}:'
            for path in paths:
                items.append((path.trim(), path))
            prompt = None
            redraw = True
        selector = self._make_selector(
            aliases=self.aliases,
            force_single_column=True,
            header=header,
            items=items,
            multiple=multiple,
            navigations=self.navigations,
            prompt=prompt,
            )
        response = selector(redraw=redraw)
        if response.payload is None:
            if self.is_navigation(response.string):
                return response.string
            elif response.string in self._get_score_names():
                return self._select_path(
                    directory,
                    infinitive=infinitive,
                    multiple=multiple,
                    scores=response.string,
                    )
            elif bool(response.string):
                self.io.display(f'matches no path {response.string!r} ...')
                return
            else:
                return
        scores = self._get_scores_directory()
        if multiple:
            assert isinstance(response.payload, list), repr(response)
            paths = [type(directory)(_) for _ in response.payload]
            paths = [scores / _.parts[0] / _ for _ in paths]
            return paths
        else:
            assert isinstance(response.payload, Path), repr(response)
            return response.payload

    def _test_external_directory(self):
        scores = abjad.abjad_configuration.composer_scores_directory
        if 'trevorbaca' in scores:
            return True
        return False

    def _to_paper_dimensions(self, paper_size, orientation='portrait'):
        prototype = ('landscape', 'portrait', None)
        assert orientation in prototype, repr(orientation)
        try:
            paper_dimensions = self._paper_size_to_paper_dimensions[paper_size]
        except KeyError:
            return 8.5, 11, 'in'
        paper_dimensions = paper_dimensions.replace(' x ', ' ')
        width, height, unit = paper_dimensions.split()
        if orientation == 'landscape':
            height_ = width
            width_ = height
            height = height_
            width = width_
        return width, height, unit

    def _trash_file(self, path):
        if path.is_file():
            self.io.display(f'trashing {path.trim()} ...')
            path.unlink()
        else:
            self.io.display(f'missing {path.trim()} ...')

    @staticmethod
    def _trim_ly(ly):
        assert ly.is_file()
        lines = []
        with ly.open() as file_pointer:
            found_score_block = False
            for line in file_pointer.readlines():
                if line.startswith(r'\score'):
                    found_score_block = True
                    continue
                if line.startswith('}'):
                    found_score_block = False
                    lines.append('\n')
                    continue
                if found_score_block:
                    lines.append(line)
        if lines and lines[0].startswith('    '):
            lines = [_[4:] for _ in lines]
        if lines and lines[-1] == '\n':
            lines.pop()
        lines = ''.join(lines)
        return lines

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self):
        r'''Gets aliases.

        Returns dictionary.
        '''
        return self._aliases

    @property
    def clipboard(self):
        r'''Gets clipboard.

        Returns list.
        '''
        return self._clipboard

    @property
    def commands(self):
        r'''Gets commands.

        Returns list.
        '''
        return self._commands

    @property
    def current_directory(self):
        r'''Gets current directory.

        Returns list.
        '''
        return self._current_directory

    @property
    def io(self):
        r'''Gets IO manager.

        Returns IO manager.
        '''
        return self._io

    @property
    def is_example(self):
        r'''Is true when IDE is example.

        Returns true, false or none.
        '''
        return self._is_example

    @property
    def is_test(self):
        r'''Is true when IDE is test.

        Returns true, false or none.
        '''
        return self._is_test

    @property
    def navigation(self):
        r'''Gets current navigation command.

        Returns string.
        '''
        return self._navigation

    @property
    def navigations(self):
        r'''Gets all navigation commands.

        Returns dictionary.
        '''
        return self._navigations

    @property
    def previous_directory(self):
        r'''Gets previous directory.

        Returns list.
        '''
        return self._previous_directory

    @property
    def terminal_dimensions(self):
        r'''Gets terminal dimensions.

        Returns pair.
        '''
        return self._terminal_dimensions

    ### PUBLIC METHODS ###

    def is_navigation(self, argument):
        r'''Is true when `argument` is navigation.

        Returns true or false.
        '''
        assert not (isinstance(argument, str) and argument == '')
        if (isinstance(argument, str) and argument in self.navigations):
            self._navigation = argument
            return True
        if argument is None:
            return True
        return False

    ### USER METHODS ###

    @Command(
        'bld',
        argument_name='directory',
        description='score pdf - build',
        directories=('build',),
        section='builds',
        )
    def build_score(self, directory):
        r'''Builds score from the ground up.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('building score ...')
        self.collect_segment_lys(directory)
        self.generate_music(directory)
        self.interpret_music(directory, open_after=False)
        tex = directory / 'front-cover.tex'
        pdf = directory / 'front-cover.pdf'
        if tex.is_file():
            self.interpret_front_cover(directory, open_after=False)
        elif pdf.is_file():
            self.io.display(f'using existing {pdf.trim()} ...')
        else:
            self.io.display('missing front cover ...')
            return
        tex = directory / 'preface.tex'
        pdf = directory / 'preface.pdf'
        if tex.is_file():
            self.interpret_preface(directory, open_after=False)
        elif pdf:
            self.io.display(f'using existing {pdf.trim()} ...')
        else:
            self.io.display('missing preface ...')
            return
        tex = directory / 'back-cover.tex'
        pdf = directory / 'back-cover.pdf'
        if tex.is_file():
            self.interpret_back_cover(directory, open_after=False)
        elif pdf.is_file():
            self.io.display(f'using existing {pdf.trim()} ...')
        else:
            self.io.display('missing back cover ...')
            return
        self.generate_score(directory)
        self.interpret_score(directory)

    @Command(
        'dfk',
        argument_name='directory',
        description='definition file - check',
        directories=('material', 'segment',),
        section='definition_file',
        )
    def check_definition_file(self, directory):
        r'''Checks definition file.

        Returns integer exit code for Travis tests.
        '''
        assert directory.is_package()
        self.io.display('checking definition file ...')
        definition = directory / 'definition.py'
        if not definition.is_file():
            self.io.display(f'missing {definition.trim()} ...')
            return
        with abjad.Timer() as timer:
            result = self.io.interpret_file(definition)
        stdout_lines, stderr_lines, exit_code = result
        self.io.display(stdout_lines)
        if exit_code:
            self.io.display([f'{definition.trim()} FAILED:'] + stderr_lines)
        else:
            self.io.display(f'{definition.trim()} ... OK', raw=True)
        self.io.display(timer.total_time_message)
        return exit_code

    @Command(
        'dfk*',
        argument_name='directory',
        description='every definition file - check',
        directories=('materials', 'segments'),
        section='star',
        )
    def check_every_definition_file(self, directory):
        r'''Checks definition file in every package.

        Returns none.
        '''
        assert directory.is_package_path(('materials', 'segments'))
        paths = directory.list_paths()
        for path in paths:
            self.check_definition_file(path)

    @Command(
        'lyc',
        argument_name='directory',
        description='segment lys - collect',
        directories=('build', 'builds',),
        section='build-preliminary',
        )
    def collect_segment_lys(self, directory):
        r'''Collects segment lys.

        Copies from segment directories to build/_segments directory.

        Trims top-level comments.

        Keeps includes and directives from each ly.

        Trims header and paper block from each ly.

        Keeps score block in each ly.

        Returns none.
        '''
        assert directory.is_package_path(('builds', 'build'))
        self.io.display('collecting segment lys ...')
        pairs = directory._collect_segment_lys()
        if not pairs:
            self.io.display('... no segment lys found.')
            return
        if not directory._segments.is_dir():
            _segments_directory.mkdir()
        for source, target in pairs:
            if target.exists():
                self.io.display(f'removing {target.trim()} ...')
            self.io.display(f'writing {target.trim()} ...')
            text = self._trim_ly(source)
            target.write_text(text)

    @Command(
        'cp',
        argument_name='directory',
        blacklist=('contents',),
        directories=True,
        external=True,
        scores=True,
        section='basic',
        )
    def copy(self, directory):
        r'''Copies into `directory`.

        Returns none.
        '''
        paths = self._select_path(
            directory, 
            infinitive='to copy',
            multiple=True,
            scores=True,
            )
        if self.is_navigation(paths):
            return
        if len(paths) == 1:
            source = paths[0]
            if source.is_contents():
                source = source.wrapper
            self.io.display(f'copying {source.trim()} ...')
            target = directory / source.name
            if source != target:
                if not self.io.confirm():
                    return
        else:
            self.io.display(f'copying ...')
            for path in paths:
                self.io.display(f'    {path.trim()}')
            if not self.io.confirm():
                return
        for source in paths:
            if source.is_contents():
                source = source.wrapper
            title = None
            name_metadatum = None
            target = directory / source.name
            if source == target:
                self.io.display(f'existing {target.trim()} ...')
                if source.is_wrapper():
                    title = self.io.get('enter title')
                    if self.is_navigation(title):
                        continue
                    name = title
                else:
                    name = self.io.get('enter new name')
                    if self.is_navigation(name):
                        continue
                name = source.parent.coerce_asset_name(
                    name,
                    suffix=source.suffix,
                    )
                target = target.with_name(name)
                if source == target:
                    continue
                if source.is_segment() and source.get_metadatum('name'):
                    name_metadatum = self.io.get('name metadatum')
                self.io.display(f'writing {target.trim()} ...')
                if not self.io.confirm():
                    continue
            if source.is_file():
                shutil.copyfile(str(source), str(target))
            elif source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                raise ValueError(source)
            if target.is_segment():
                if name_metadatum:
                    target.add_metadatum('name', name_metadatum)
                else:
                    target.remove_metadatum('name')
            elif target.is_wrapper():
                shutil.move(
                    str(target.wrapper / source.name),
                    str(target.contents),
                    )
                lines = self._replace_in_tree(
                    target,
                    source.name,
                    target.name,
                    complete_words=True,
                    )
                self.io.display(lines)
                if title is not None:
                    target.contents.add_metadatum('title', title)
                    source_title = source.contents.get_metadatum('title')
                    if source_title is not None:
                        lines = self._replace_in_tree(
                            target,
                            source_title,
                            title,
                            complete_words=True,
                            )
                        self.io.display(lines)

    @Command(
        'pc',
        argument_name='directory',
        directories=True,
        external=True,
        scores=True,
        section='clipboard',
        )
    def copy_to_clipboard(self, directory):
        r'''Copies to clipboard.

        Returns none.
        '''
        paths = self._select_path(
            directory, 
            infinitive='for clipboard',
            multiple=True,
            scores=False,
            )
        if self.is_navigation(paths):
            return
        self.io.display('copying to clipboard ...')
        for path in paths:
            self.io.display(path.trim(), raw=True)
            self.clipboard.append(path)

    @Command(
        '?',
        directories=True,
        external=True,
        section='system',
        scores=True,
        )
    def display_action_command_help(self):
        r'''Displays action command help.

        Returns none.
        '''
        pass

    @Command(
        ';',
        directories=True,
        external=True,
        scores=True,
        section='display navigation',
        )
    def display_navigation_command_help(self):
        r'''Displays navigation command help.

        Returns none.
        '''
        pass

    @Command(
        'als',
        description='aliases - edit',
        directories=True,
        external=True,
        scores=True,
        section='global files',
        )
    def edit_aliases_file(self):
        r'''Edits aliases file.

        Returns none.
        '''
        self._open_file(self.configuration.aliases_file_path)
        self.configuration._read_aliases_file()
        self._aliases = dict(self.configuration.aliases)

    @Command(
        'bce',
        argument_name='directory',
        description='back cover - edit',
        directories=('build',),
        section='build-edit',
        )
    def edit_back_cover_source(self, directory):
        r'''Edits ``back-cover.tex`` in `directory`.

        Returns none.
        '''
        directory.is_build()
        self._open_file(directory / 'back-cover.tex')

    @Command(
        'df',
        argument_name='directory',
        description='definition file - edit',
        directories=('material', 'segment',),
        section='definition_file',
        )
    def edit_definition_file(self, directory):
        r'''Edits definition file.

        Returns none.
        '''
        assert directory.is_package()
        self._open_file(directory / 'definition.py')

    @Command(
        'df*',
        argument_name='directory',
        description='every definition file - edit',
        directories=('materials', 'segments'),
        section='star',
        )
    def edit_every_definition_file(self, directory):
        r'''Edits definition file `directory` tree.

        Returns none.
        '''
        assert directory.is_package_path(('materials', 'segments'))
        paths = directory.list_paths()
        paths = [_ / 'definition.py' for _ in paths]
        self._open_every_file(paths)

    @Command(
        'ff*',
        argument_name='directory',
        description='every file - edit',
        directories=True,
        external=True,
        scores=True,
        section='star',
        )
    def edit_every_file(self, directory):
        r'''Edits every file in `directory` tree.

        Returns none.
        '''
        name = self.io.get('enter filename')
        if self.is_navigation(name):
            return
        command = f'find {directory!s} -name {name}'
        paths = self.io.run_command(command)
        if not paths:
            self.io.display(f'missing {name!r} files ...')
        else:
            paths = [Path(_) for _ in paths]
            self._open_every_file(paths)

    @Command(
        'ee*',
        argument_name='directory',
        description='every string - edit',
        directories=True,
        external=True,
        scores=True,
        section='star',
        )
    def edit_every_string(self, directory):
        r'''Opens Vim and goes to every occurrence of search string.

        Returns none.
        '''
        search_string = self.io.get('enter search string')
        if self.is_navigation(search_string):
            return
        command = rf'vim -c "grep {search_string!s} --type=python"'
        if self.is_test:
            return
        with self.io.change(directory):
            self.io.spawn_subprocess(command)

    @Command(
        'fce',
        argument_name='directory',
        description='front cover - edit',
        directories=('build',),
        section='build-edit',
        )
    def edit_front_cover_source(self, directory):
        r'''Edits ``front-cover.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'front-cover.tex')

    @Command(
        'ill',
        argument_name='directory',
        description='illustrate file - edit',
        directories=('material',),
        section='illustrate_file',
        )
    def edit_illustrate_file(self, directory):
        r'''Edits illustrate file.

        Returns none.
        '''
        assert directory.is_material()
        self._open_file(directory / '__illustrate__.py')

    @Command(
        'lxg',
        description='latex log - edit',
        directories=True,
        external=True,
        scores=True,
        section='global files',
        )
    def edit_latex_log(self):
        r'''Edits LaTeX log.

        Returns none.
        '''
        self._open_file(self.configuration.latex_log_file_path)

    @Command(
        'lpg',
        description='lilypond log - edit',
        directories=True,
        external=True,
        scores=True,
        section='global files',
        )
    def edit_lilypond_log(self):
        r'''Edits LilyPond log.

        Returns none.
        '''
        target = abjad.abjad_configuration.lilypond_log_file_path
        self._open_file(Path(target))

    @Command(
        'ly',
        argument_name='directory',
        description='ly - edit',
        directories=('material', 'segment',),
        section='ly',
        )
    def edit_ly(self, directory):
        r'''Edits ``illustration.ly`` in `directory`.

        Returns none.
        '''
        assert directory.is_package()
        self._open_file(directory / 'illustration.ly')

    @Command(
        'me',
        argument_name='directory',
        description='music - edit',
        directories=('build',),
        section='build-edit',
        )
    def edit_music_source(self, directory):
        r'''Edits ``music.ly`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'music.ly')

    @Command(
        're',
        argument_name='directory',
        description='preface - edit',
        directories=('build',),
        section='build-edit',
        )
    def edit_preface_source(self, directory):
        r'''Edits ``preface.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'preface.tex')

    @Command(
        'se',
        argument_name='directory',
        description='score - edit',
        directories=('build',),
        section='build-edit',
        )
    def edit_score_source(self, directory):
        r'''Edits ``score.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'score.tex')

    @Command(
        'ste',
        argument_name='directory',
        description='stylesheet - edit',
        directories=('build',),
        section='build-edit',
        )
    def edit_stylesheet(self, directory):
        r'''Edits ``stylesheet.ily`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'stylesheet.ily')

    @Command(
        'pe',
        argument_name='directory',
        directories=True,
        external=True,
        scores=True,
        section='clipboard',
        )
    def empty_clipboard(self, directory):
        r'''Empties clipboard.

        Returns none.
        '''
        if not bool(self.clipboard):
            self.io.display('clipboard is empty ...')
            return
        self.io.display('emptying clipboard ...')
        for path in self.clipboard:
            self.io.display(path.trim())
        self._clipboard[:] = []

    @Command(
        'bcg',
        argument_name='directory',
        description='back cover - generate',
        directories=('build',),
        section='build-generate',
        )
    def generate_back_cover(self, directory):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('generating back cover ...')
        values = {}
        contents = directory.contents
        catalog_number = contents.get_metadatum('catalog_number')
        name = 'catalog_number_suffix'
        catalog_number_suffix = contents.get_metadatum(name)
        if catalog_number_suffix:
            catalog_number += f' / {catalog_number_suffix}'
        values['catalog_number'] = catalog_number
        composer_website = abjad.abjad_configuration.composer_website or ''
        if self.is_test or self.is_example:
            composer_website = 'www.composer-website.com'
        values['composer_website'] = composer_website
        price = contents.get_metadatum('price', r'\null')
        values['price'] = price
        paper_size = contents.get_metadatum('paper_size', 'letter')
        orientation = contents.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        self._copy_boilerplate(directory, 'back-cover.tex', values=values)

    @Command(
        'stg',
        argument_name='directory',
        description='stylesheet - generate',
        directories=('build',),
        section='build-generate',
        )
    def generate_build_stylesheet(self, directory):
        r'''Generates build directory ``stylsheet.ily``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('generating stylesheet ...')
        values = {}
        paper_size = directory.get_metadatum('paper_size')
        values['paper_size'] = paper_size
        orientation = directory.get_metadatum('orientation')
        if orientation:
            orientation_ = f" '{orientation}"
        else:
            orientation_ = ''
        values['orientation'] = orientation_
        self._copy_boilerplate(
            directory,
            'build-directory-stylesheet.ily',
            target_name='stylesheet.ily',
            values=values,
            )

    @Command(
        'fcg',
        argument_name='directory',
        description='front cover - generate',
        directories=('build',),
        section='build-generate',
        )
    def generate_front_cover(self, directory):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        assert directory.is_build()
        contents = directory.contents
        self.io.display('generating front cover ...')
        file_name = 'front-cover.tex'
        values = {}
        score_title = contents.get_title(year=False)
        score_title = score_title.upper()
        values['score_title'] = score_title
        forces_tagline = contents.get_metadatum('forces_tagline', '')
        values['forces_tagline'] = forces_tagline
        year = contents.get_metadatum('year', '')
        values['year'] = str(year)
        composer = abjad.abjad_configuration.composer_uppercase_name
        if (self.is_test or self.is_example):
            composer = 'COMPOSER'
        values['composer'] = str(composer)
        paper_size = contents.get_metadatum('paper_size', 'letter')
        orientation = contents.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        self._copy_boilerplate(directory, file_name, values=values)

    @Command(
        'mg',
        argument_name='directory',
        description='music - generate',
        directories=('build',),
        section='build-generate',
        )
    def generate_music(self, directory):
        r'''Generates ``music.ly``.

        Returns none.
        '''
        assert directory.is_build()
        contents = directory.contents
        self.io.display('generating music ...')
        target = directory / 'music.ly'
        if target.exists():
            self.io.display(f'removing {target.trim()} ...')
            target.unlink()
        paths = contents.segments.list_paths()
        if paths:
            view = contents.segments.get_metadatum('view')
            if bool(view):
                self.io.display(f'examining segments in view order ...')
            else:
                self.io.display('examining segments alphabetically ...')
        else:
            self.io.display('no segments found ...')
        for path in paths:
            self.io.display(f'examining {path.trim()} ...')
        names = [_.stem.replace('_', '-') for _ in paths]
        source = Path('boilerplate') / 'music.ly'
        self.io.display(f'writing {target.trim()} ...')
        shutil.copyfile(str(source), str(target))
        lines = []
        segment_include_statements = ''
        for i, name in enumerate(names):
            name += '.ly'
            path = directory._segments / name
            if path.is_file():
                line = rf'\include "../_segments/{name}"'
            else:
                line = rf'%\include "../_segments/{name}"'
            if 0 < i:
                line = 4 * ' ' + line
            lines.append(line)
        if lines:
            new = '\n'.join(lines)
            segment_include_statements = new
        stylesheet_include_statement = ''
        if directory.is_builds():
            line = r'\include "../stylesheets/stylesheet.ily"'
        elif directory.is_build():
            line = r'\include "stylesheet.ily"'
        stylesheet_include_statement = line
        language_token = abjad.LilyPondLanguageToken()
        lilypond_language_directive = format(language_token)
        version_token = abjad.LilyPondVersionToken()
        lilypond_version_directive = format(version_token)
        annotated_title = contents.get_title(year=True)
        if annotated_title:
            score_title = annotated_title
        else:
            score_title = contents.get_title(year=False)
        forces_tagline = contents.get_metadatum('forces_tagline', '')
        template = target.read_text()
        template = template.format(
            forces_tagline=forces_tagline,
            lilypond_language_directive=lilypond_language_directive,
            lilypond_version_directive=lilypond_version_directive,
            score_title=score_title,
            segment_include_statements=segment_include_statements,
            stylesheet_include_statement=stylesheet_include_statement,
            )
        target.write_text(template)

    @Command(
        'rg',
        argument_name='directory',
        description='preface - generate',
        directories=('build',),
        section='build-generate',
        )
    def generate_preface(self, directory):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('generating preface ...')
        values = {}
        paper_size = directory.get_metadatum('paper_size', 'letter')
        orientation = directory.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        self._copy_boilerplate(directory, 'preface.tex', values=values)

    @Command(
        'sg',
        argument_name='directory',
        description='score - generate',
        directories=('build',),
        section='build-generate',
        )
    def generate_score(self, directory):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('generating score ...')
        values = {}
        paper_size = directory.get_metadatum('paper_size', 'letter')
        orientation = directory.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        self._copy_boilerplate(directory, 'score.tex', values=values)

    @Command(
        'ci',
        argument_name='directory',
        description='git - commit',
        directories=True,
        external=True,
        section='git',
        )
    def git_commit(self, directory, commit_message=None):
        r'''Commits working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.io.change(root):
            self.io.display(f'git commit {root} ...')
            if not root._has_pending_commit():
                self.io.display(f'{root} ... nothing to commit.')
                return
            self.io.spawn_subprocess('git status .')
            if self.is_test:
                return
            command = f'git add -A {root}'
            lines = self.io.run_command(command)
            self.io.display(lines, raw=True)
            if commit_message is None:
                commit_message = self.io.get('commit message')
                if self.is_navigation(commit_message):
                    return
            command = f'git commit -m "{commit_message}" {root}'
            command += '; git push'
            lines = self.io.run_command(command)
            self.io.display(lines, raw=True)

    @Command(
        'ci*',
        argument_name='directory',
        description='every package - git commit',
        scores=True,
        section='git',
        )
    def git_commit_every_package(self, directory):
        r'''Commits every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        commit_message = self.io.get('commit message')
        if self.is_navigation(commit_message):
            return
        paths = directory.list_paths()
        for path in paths:
            self.git_commit(path, commit_message=commit_message)

    @Command(
        'diff',
        argument_name='directory',
        description='git - diff',
        directories=True,
        external=True,
        section='git',
        )
    def git_diff(self, directory):
        r'''Displays Git diff of working copy.

        Returns none.
        '''
        if not directory._get_repository_root():
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.io.change(directory):
            self.io.spawn_subprocess(f'git diff {directory}')

    @Command(
        'pull',
        argument_name='directory',
        description='git - pull',
        directories=True,
        external=True,
        section='git',
        )
    def git_pull(self, directory):
        r'''Pulls working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.io.change(root):
            self.io.display(f'git pull {root} ...')
            if not self.is_test:
                lines = self.io.run_command('git pull .')
                if lines and 'Already up-to-date' in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)
                command = 'git submodule foreach git pull origin master'
                self.io.display(f'{command} ...')
                lines = self.io.run_command(command)
                if lines and 'Already up-to-date' in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)

    @Command(
        'pull*',
        argument_name='directory',
        description='every package - git pull',
        scores=True,
        section='git',
        )
    def git_pull_every_package(self, directory):
        r'''Pulls every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        for path in directory.list_paths():
            self.git_pull(path)

    @Command(
        'push',
        argument_name='directory',
        description='git - push',
        directories=True,
        external=True,
        section='git',
        )
    def git_push(self, directory):
        r'''Pushes working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.io.change(root):
            self.io.display(f'git push {root} ...')
            if not self.is_test:
                self.io.spawn_subprocess('git push .')

    @Command(
        'push*',
        argument_name='directory',
        description='every package - git push',
        scores=True,
        section='git',
        )
    def git_push_every_package(self, directory):
        r'''Pushes every package.

        Returns none.
        '''
        assert directory.is_scores()
        for path in directory.list_paths():
            self.git_push(path)

    @Command(
        'st',
        argument_name='directory',
        description='git - status',
        directories=True,
        external=True,
        section='git',
        )
    def git_status(self, directory):
        r'''Displays Git status of working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.io.change(root):
            self.io.display(f'git status {root} ...')
            self.io.spawn_subprocess('git status .')
            self.io.display('')
            command = 'git submodule foreach git fetch'
            self.io.display(f'{command} ...')
            self.io.spawn_subprocess(command)

    @Command(
        'st*',
        argument_name='directory',
        description='every package - git status',
        scores=True,
        section='git',
        )
    def git_status_every_package(self, directory):
        r'''Displays Git status of every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        for path in directory.list_paths():
            self.git_status(path)

    @Command(
        '-',
        description='back',
        directories=True,
        external=True,
        scores=True,
        section='back-home-quit',
        )
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        if self.previous_directory:
            self._manage_directory(self.previous_directory)

    @Command(
        'bb',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_builds_directory(self, directory):
        r'''Goes to builds directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.builds)

    @Command(
        'nn',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_builds_segments_directory(self, directory):
        r'''Goes to builds/_segments directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory._segments)

    @Command(
        'cc',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_contents_directory(self, directory):
        r'''Goes to contents directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.contents)

    @Command(
        'dd',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_distribution_directory(self, directory):
        r'''Goes to distribution directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.distribution)

    @Command(
        'ee',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_etc_directory(self, directory):
        r'''Goes to etc directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.etc)

    @Command(
        'lib',
        directories=True,
        external=True,
        scores=True,
        section='scores',
        )
    def go_to_library(self):
        r'''Goes to library.

        Returns none.
        '''
        directory = self._get_library()
        if directory is None:
            self.io.display('missing library ...')
        else:
            self._manage_directory(directory)

    @Command(
        'mm',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_materials_directory(self, directory):
        r'''Goes to materials directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.materials)

    @Command(
        '>',
        argument_name='directory',
        directories=('material', 'materials', 'segment', 'segments'),
        section='sibling navigation',
        )
    def go_to_next_package(self, directory):
        r'''Goes to next package.

        Returns none.
        '''
        prototype = ('material', 'materials', 'segment', 'segments',)
        assert directory.is_package_path(prototype)
        directory = directory.get_next_package(cyclic=True)
        self._manage_directory(directory)

    @Command(
        '<',
        argument_name='directory',
        directories=('material', 'materials', 'segment', 'segments',),
        section='sibling navigation',
        )
    def go_to_previous_package(self, directory):
        r'''Goes to previous package.

        Returns none.
        '''
        prototype = ('material', 'materials', 'segment', 'segments')
        assert directory.is_package_path(prototype)
        directory = directory.get_previous_package(cyclic=True)
        self._manage_directory(directory)

    @Command(
        'ss',
        directories=True,
        external=True,
        scores=True,
        section='scores',
        )
    def go_to_scores_directory(self):
        r'''Goes to scores directory.

        Returns none.
        '''
        directory = self.configuration.composer_scores_directory
        if self.is_test or self.is_example:
            directory = self.configuration.test_scores_directory
        self._manage_directory(directory)

    @Command(
        'gg',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_segments_directory(self, directory):
        r'''Goes to segments directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.segments)

    @Command(
        'yy',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_stylesheets_directory(self, directory):
        r'''Goes to stylesheets directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.stylesheets)

    @Command(
        'tt',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_test_directory(self, directory):
        r'''Goes to test directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.test)

    @Command(
        'oo',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_tools_directory(self, directory):
        r'''Goes to tools directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.tools)

    @Command(
        'ww',
        argument_name='directory',
        directories=True,
        section='navigation',
        )
    def go_to_wrapper_directory(self, directory):
        r'''Goes to wrapper directory.

        Returns none.
        '''
        assert directory.is_package_path()
        self._manage_directory(directory.wrapper)

    @Command(
        '..',
        description='up',
        directories=True,
        external=True,
        scores=True,
        section='back-home-quit',
        )
    def go_up(self):
        r'''Goes up.

        Returns none.
        '''
        if self.current_directory:
            self._manage_directory(self.current_directory.parent)

    @Command(
        'bci',
        argument_name='directory',
        description='back cover - interpret',
        directories=('build',),
        section='build-interpret',
        )
    def interpret_back_cover(self, directory, open_after=True):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('interpreting back cover ...')
        source = directory / 'back-cover.tex'
        target = source.with_suffix('.pdf')
        self._interpret_tex_file(source)
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        'lyi*',
        argument_name='directory',
        description='every ly - interpret',
        directories=('materials', 'segments',),
        section='star',
        )
    def interpret_every_ly(self, directory):
        r'''Interprets LilyPond file in every directory.

        Makes PDF in every directory.

        Returns none.
        '''
        assert directory.is_package_path(('materials', 'segments'))
        self.io.display('interpreting every ly ...')
        paths = directory.list_paths()
        sources = []
        for path in paths:
            source = path / 'illustration.ly'
            if source.is_file():
                sources.append(source)
        if not sources:
            self.io.display('no LilyPond files found.')
            return
        with abjad.Timer() as timer:
            for source in sources:
                self.interpret_ly(source.parent, open_after=False)
            self.io.display(timer.total_time_message)

    @Command(
        'fci',
        argument_name='directory',
        description='front cover - interpret',
        directories=('build',),
        section='build-interpret',
        )
    def interpret_front_cover(self, directory, open_after=True):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('interpreting front cover ...')
        source = directory / 'front-cover.tex'
        target = source.with_suffix('.pdf')
        self._interpret_tex_file(source)
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        'lyi',
        argument_name='directory',
        description='ly - interpret',
        directories=('material', 'segment',),
        section='ly',
        )
    def interpret_ly(self, directory, open_after=True):
        r'''Interprets illustration ly in `directory`.

        Makes illustration PDF.

        Returns none.
        '''
        assert directory.is_package()
        self.io.display('interpreting ly ...')
        source = directory / 'illustration.ly'
        target = source.with_suffix('.pdf')
        if source.is_file():
            self._run_lilypond(source)
        else:
            self.io.display(f'missing {source.trim()} ...')
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        'mi',
        argument_name='directory',
        description='music - interpret',
        directories=('build',),
        section='build-interpret',
        )
    def interpret_music(self, directory, open_after=True):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('interpreting music ...')
        source = directory / 'music.ly'
        target = source.with_suffix('.pdf')
        if not source.is_file():
            self.io.display(f'can not find {source.trim()} ...')
            return
        self._run_lilypond(source)
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        'ri',
        argument_name='directory',
        description='preface - interpret',
        directories=('build',),
        section='build-interpret',
        )
    def interpret_preface(self, directory, open_after=True):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('interpreting preface ...')
        source = directory / 'preface.tex'
        target = source.with_suffix('.pdf')
        self._interpret_tex_file(source)
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        'si',
        argument_name='directory',
        description='score - interpret',
        directories=('build',),
        section='build-interpret',
        )
    def interpret_score(self, directory, open_after=True):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        assert directory.is_build()
        self.io.display('interpreting score ...')
        source = directory / 'score.tex'
        target = source.with_suffix('.pdf')
        self._interpret_tex_file(source)
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        '!',
        directories=True,
        external=True,
        scores=True,
        section='system',
        )
    def invoke_shell(self, directory):
        r'''Invokes shell.

        Returns none.
        '''
        pass

    @Command(
        'pdfm*',
        argument_name='directory',
        description='every pdf - make',
        directories=('materials', 'segments',),
        section='star',
        )
    def make_every_pdf(self, directory):
        r'''Makes PDF in every directory.

        Returns none.
        '''
        assert directory.is_package_path(('materials', 'segments'))
        for path in directory.list_paths():
            self.make_pdf(path, open_after=False)

    @Command(
        'illm',
        argument_name='directory',
        description='illustrate file - make',
        directories=('material',),
        section='illustrate_file',
        )
    def make_illustrate_file(self, directory):
        r'''Makes illustrate file.

        Returns none.
        '''
        assert directory.is_material()
        source = Path('boilerplate')
        source /= '__illustrate_material__.py'
        target = directory / '__illustrate__.py'
        if target.is_file():
            self.io.display(f'preserving {target.trim()} ...')
            return
        self.io.display(f'writing {target.trim()} ...')
        shutil.copyfile(str(source), str(target))
        template = target.read_text()
        template = template.format(
            score_package_name=directory.contents.name,
            material_package_name=directory.name,
            )
        target.write_text(template)

    @Command(
        'lym',
        argument_name='directory',
        description='ly - make',
        directories=('material', 'segment',),
        section='ly',
        )
    def make_ly(self, directory):
        r'''Makes illustration ly.

        Returns none.
        '''
        assert directory.is_package()
        self.io.display('making ly ...')
        if directory.is_material():
            self._make_material_ly(directory)
        elif directory.is_segment():
            self._make_segment_ly(directory)
        else:
            raise ValueError(directory)

    @Command(
        'midim',
        argument_name='directory',
        description='midi - make',
        directories=('segment',),
        section='midi',
        )
    def make_midi(self, directory, open_after=True):
        r'''Makes segment MIDI file.

        Returns integer exit code for Travis tests.
        '''
        assert directory.is_segment()
        return self._make_segment_midi(directory, open_after=open_after)

    @Command(
        'pdfm',
        argument_name='directory',
        description='pdf - make',
        directories=('material', 'segment',),
        section='pdf',
        )
    def make_pdf(self, directory, open_after=True):
        r'''Makes illustration PDF.

        Returns integer exit code for Travis tests.
        '''
        assert directory.is_package()
        if directory.is_material():
            return self._make_material_pdf(
                directory,
                open_after=open_after,
                )
        elif directory.is_segment():
            return self._make_segment_pdf(directory, open_after=open_after)
        else:
            raise ValueError(directory)

    @Command(
        'new',
        argument_name='directory',
        blacklist=('contents',),
        directories=True,
        external=True,
        scores=True,
        section='basic',
        )
    def new(self, directory):
        r'''Makes asset.

        Returns none.
        '''
        if directory.is_scores():
            self._make_score_package()
        elif directory.is_package_path(('materials', 'segments')):
            self._make_package(directory)
        elif directory.is_builds():
            self._make_build_directory(directory)
        else:
            self._make_file(directory)

    @Command(
        'bco',
        argument_name='directory',
        description='back cover - open',
        directories=('build',),
        section='build-open',
        )
    def open_back_cover_pdf(self, directory):
        r'''Opens ``back-cover.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'back-cover.pdf')

    @Command(
        'pdf*',
        argument_name='directory',
        description='every pdf - open',
        directories=True,
        external=True,
        scores=True,
        section='star',
        )
    def open_every_pdf(self, directory):
        r'''Opens PDF in every package.

        Returns none.
        '''
        pdfs = []
        if directory.is_scores():
            for path in directory.list_paths():
                pdf = path._get_score_pdf()
                if pdf is None:
                    continue
                pdfs.append(pdf)
        else:
            for path in directory.list_paths():
                if path.suffix == '.pdf':
                    pdfs.append(path)
                elif path.is_dir():
                    for pdf_ in path.glob('*.pdf'):
                        pdfs.append(pdf_)
        if not pdfs:
            self.io.display('missing PDFs ...')
        else:
            self._open_every_file(pdfs)

    @Command(
        'fco',
        argument_name='directory',
        description='front cover - open',
        directories=('build',),
        section='build-open',
        )
    def open_front_cover_pdf(self, directory):
        r'''Opens ``front-cover.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'front-cover.pdf')

    @Command(
        'mo',
        argument_name='directory',
        description='music - open',
        directories=('build',),
        section='build-open',
        )
    def open_music_pdf(self, directory):
        r'''Opens ``music.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'music.pdf')

    @Command(
        'pdfo',
        argument_name='directory',
        description='pdf - open',
        directories=('material', 'segment',),
        section='pdf',
        )
    def open_pdf(self, directory):
        r'''Opens illustration PDF.

        Returns none.
        '''
        assert directory.is_package()
        self._open_file(directory / 'illustration.pdf')

    @Command(
        'ro',
        argument_name='directory',
        description='preface - open',
        directories=('build',),
        section='build-open',
        )
    def open_preface_pdf(self, directory):
        r'''Opens ``preface.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'preface.pdf')

    @Command(
        'spdfo',
        argument_name='directory',
        description='score pdf - open',
        directories=True,
        section='pdf',
        )
    def open_score_pdf(self, directory):
        r'''Opens ``score.pdf``.

        Returns score PDF path.
        '''
        assert directory.is_package_path()
        path = directory._get_score_pdf()
        if path:
            self._open_file(path)
        else:
            message = 'missing score PDF'
            message += ' in distribution and build directories ...'
            self.io.display(message)

    @Command(
        'so',
        argument_name='directory',
        description='score - open',
        directories=('build',),
        section='build-open',
        )
    def open_score_pdf_in_build_directory(self, directory):
        r'''Opens ``score.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is_build()
        self._open_file(directory / 'score.pdf')

    @Command(
        'pv',
        argument_name='directory',
        directories=True,
        external=True,
        scores=True,
        section='clipboard',
        )
    def paste_from_clipboard(self, directory):
        r'''Pastes from clipboard.

        Returns none.
        '''
        if not bool(self.clipboard):
            self.io.display('showing empty clipboard ...')
            return
        self.io.display('pasting from clipboard ...')
        for i, source in enumerate(self.clipboard[:]):
            self.io.display(f'    {source.trim()} ...')
            target = directory / source.name
            self.io.display(f'    {target.trim()} ...')
            if target.exists():
                self.io.display(['', f'existing {target.trim()} ...'])
                name = self.io.get('enter new name')
                if self.is_navigation(name):
                    return
                if not bool(name):
                    continue
                target = target.with_name(name)
                if target.exists():
                    self.io.display(f'existing {target.trim()} ...')
                    return
                self.io.display(f'    {source.trim()} ...')
                self.io.display(f'    {target.trim()} ...')
            if source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                shutil.copy(str(source), str(target))
            if i < len(self.clipboard) - 1:
                self.io.display('')

    @Command(
        'q',
        description='quit',
        directories=True,
        external=True,
        scores=True,
        section='back-home-quit',
        )
    def quit(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._navigation = 'q'

    @Command(
        'rm',
        argument_name='directory',
        blacklist=('contents',),
        directories=True,
        external=True,
        scores=True,
        section='basic',
        )
    def remove(self, directory):
        r'''Removes file or directory.

        Returns none.
        '''
        paths = self._select_path(
            directory,
            infinitive='to remove',
            multiple=True,
            scores=False,
            )
        if self.is_navigation(paths):
            return
        count = len(paths)
        if count == 1:
            if paths[0].is_contents():
                path_ = paths[0].wrapper
            else:
                path_ = paths[0]
            self.io.display(f'confirming {path_.trim()} ...')
        else:
            self.io.display('confirming ...')
            for path in paths:
                if path.is_contents():
                    path_ = path.wrapper
                else:
                    path_ = path
                self.io.display(f'    {path_.trim()}')
        if count == 1:
            string = 'remove'
        else:
            string = f'remove {count}'
        result = self.io.get(f"type {string!r} to proceed")
        if self.is_navigation(result) or result != string:
            return
        for path in paths:
            if path.is_contents():
                path = path.wrapper
            self.io.display(f'removing {path.trim()} ...')
            path.remove()

    @Command(
        'ren',
        argument_name='directory',
        blacklist=('contents',),
        directories=True,
        external=True,
        scores=True,
        section='basic',
        )
    def rename(self, directory):
        r'''Renames asset.

        Returns none.
        '''
        source = self._select_path(
            directory,
            infinitive='to rename',
            multiple=False,
            scores=False,
            )
        if self.is_navigation(source):
            return
        if source.is_contents():
            source = source.parent
        self.io.display(f'renaming {source.trim()} ...')
        target = self.io.get('new name')
        if self.is_navigation(target):
            return
        original_target_name = target
        target = directory.coerce_asset_name(target)
        target = source.parent / target
        if target.exists():
            self.io.display(f'existing {target.trim()!r} ...')
            return
        self.io.display('Renaming ...')
        self.io.display(f' FROM: {source.trim()}')
        self.io.display(f'   TO: {target.trim()}')
        if not self.io.confirm():
            return
        shutil.move(str(source), str(target))
        if target.is_dir():
            for path in sorted(target.glob('*.py')):
                self._replace_in_file(path, source.name, target.name)
        if target.is_wrapper():
            false_contents_directory = target / source.name
            assert false_contents_directory.exists()
            true_contents_directory = target / target.name
            shutil.move(
                str(false_contents_directory),
                str(true_contents_directory),
                )
            true_contents_directory.add_metadatum(
                'title',
                original_target_name,
                )
            for path in sorted(true_contents_directory.glob('*.py')):
                self._replace_in_file(path, source.name, target.name)

    @Command(
        'rp',
        argument_name='directory',
        directories=True,
        external=True,
        scores=True,
        section='system',
        )
    def replace(self, directory):
        r'''Replaces search string with replace string.

        Returns none.
        '''
        search_string = self.io.get('enter search string')
        if self.is_navigation(search_string):
            return
        replace_string = self.io.get('enter replace string')
        if self.is_navigation(replace_string):
            return
        complete_words = False
        result = self.io.confirm('complete words only?')
        if result:
            complete_words = True
        if directory == directory.scores:
            pass
        else:
            directory = directory.wrapper
        lines = self._replace_in_tree(
            directory,
            search_string,
            replace_string,
            complete_words,
            )
        self.io.display(lines, raw=True)

    @Command(
        'dt',
        argument_name='directory',
        description='doctest - run',
        directories=True,
        external=True,
        scores=True,
        section='tests',
        )
    def run_doctest(self, directory):
        r'''Runs doctest.

        Returns none.
        '''
        with self.io.change(directory):
            self._run_doctest(directory)

    @Command(
        'pt',
        argument_name='directory',
        description='pytest - run',
        directories=True,
        external=True,
        scores=True,
        section='tests',
        )
    def run_pytest(self, directory):
        r'''Runs pytest from contents directory.

        Returns none.
        '''
        with self.io.change(directory):
            self._run_pytest(directory)

    @Command(
        'tests',
        argument_name='directory',
        description='tests - run',
        directories=True,
        external=True,
        scores=True,
        section='tests',
        )
    def run_tests(self, directory):
        r'''Runs doctest and pytest from contents directory.

        Returns none.
        '''
        self.run_doctest(directory)
        self.run_pytest(directory)

    @Command(
        'sr',
        argument_name='directory',
        directories=True,
        external=True,
        scores=True,
        section='system',
        )
    def search(self, directory):
        r'''Searches for expression

        Delegates to ack if ack is found.

        Delegates to grep is ack is not found.

        Returns none.
        '''
        executables = self.io.find_executable('ack')
        if not executables:
            executables = self.io.find_executable('grep')
        executables = [Path(_) for _ in executables]
        if not executables:
            self.io.display('can not find ack.')
            self.io.display('can not find grep.')
            return
        assert 1 <= len(executables)
        executable = None
        for path in executables:
            if path.is_file():
                executable = path
        if executable is None:
            self.io.display('can not find ack.')
            self.io.display('can not find grep.')
            return
        search_string = self.io.get('enter search string')
        if self.is_navigation(search_string):
            return
        if executable.name == 'ack':
            command = r'{!s} --ignore-dir=_docs {} --type=python'
            command = command.format(executable, search_string)
        elif executable.name == 'grep':
            command = rf'{executable!s} -r {search_string!r} *'
        if directory.wrapper is not None:
            directory = directory.wrapper
        with self.io.change(directory):
            lines = self.io.run_command(command)
            self.io.display(lines, raw=True)

    @Command(
        'ps',
        argument_name='directory',
        directories=True,
        external=True,
        scores=True,
        section='clipboard',
        )
    def show_clipboard(self, directory):
        r'''Shows clipboard.

        Returns none.
        '''
        if not bool(self.clipboard):
            self.io.display('showing empty clipboard ...')
            return
        self.io.display('showing clipboard ...')
        for path in self.clipboard:
            self.io.display(path.trim(), raw=True)

#    @Command(
#        'illt',
#        argument_name='directory',
#        description='illustrate file - trash',
#        directories=('material',),
#        section='illustrate_file',
#        )
#    def trash_illustrate(self, directory):
#        r'''Trashes illustration file.
#
#        Returns none.
#        '''
#        assert directory.is_material()
#        self._trash_file(directory / '__illustrate__.py')

#    @Command(
#        'lyt',
#        argument_name='directory',
#        description='ly - trash',
#        directories=('material', 'segment',),
#        section='ly',
#        )
#    def trash_ly(self, directory):
#        r'''Trashes illustration LilyPond file.
#
#        Returns none.
#        '''
#        assert directory.is_package()
#        self._trash_file(directory / 'illustration.ly')

#    @Command(
#        'trash',
#        argument_name='directory',
#        description='ly & pdf - trash',
#        directories=('material', 'segment',),
#        section='ly & pdf',
#        )
#    def trash_ly_and_pdf(self, directory):
#        r'''Trashes illustration LilyPond file and illustration PDF.
#
#        Returns none.
#        '''
#        assert directory.is_package()
#        self._trash_file(directory / 'illustration.ly')
#        self._trash_file(directory / 'illustration.pdf')

#    @Command(
#        'pdft',
#        argument_name='directory',
#        description='pdf - trash',
#        directories=('material', 'segment',),
#        section='pdf',
#        )
#    def trash_pdf(self, directory):
#        r'''Trashes illustration PDF.
#
#        Returns none.
#        '''
#        assert directory.is_package()
#        self._trash_file(directory / 'illustration.pdf')
