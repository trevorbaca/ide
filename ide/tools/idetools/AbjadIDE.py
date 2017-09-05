import abjad
import datetime
import importlib
import inspect
import pathlib
import shutil
from ide.tools.idetools.Command import Command


class AbjadIDE(abjad.AbjadObject):
    r'''Abjad IDE.

    ::

        >>> import ide

    ..  container:: example

        ::

            >>> abjad_ide = ide.AbjadIDE()
            >>> abjad_ide
            AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_current_directory',
        '_io_manager',
        '_previous_directory',
        )

    _addressing_characters = ('@', '%', '^', '*')

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

    ### INITIALIZER ###

    def __init__(self, is_example=False, is_test=False):
        from ide.tools.idetools.IOManager import IOManager
        self._io_manager = IOManager(is_example=is_example, is_test=is_test)
        self._check_test_scores_directory(is_example or is_test)
        self._current_directory = None
        self._previous_directory = None

    ### SPECIAL METHODS ###

    def __call__(self, string=None):
        r'''Calls IDE on `string`.

        Returns none.
        '''
        self.io_manager._is_quitting = None
        self.io_manager._pending_input = string
        self.io_manager._transcript.__init__()
        scores = self.io_manager.configuration.composer_scores_directory
        if (self.io_manager._is_test or
            self.io_manager._is_example):
            scores = self.io_manager.configuration.test_scores_directory
        while True:
            self._manage_directory(scores)
            if self.io_manager._is_quitting:
                break
        self.io_manager._clean_up()
        self.io_manager.clear_terminal()

    def __repr__(self):
        r'''Gets interpreter representation of AbjadIDE.

        Returns string.
        '''
        return f'{type(self).__name__}()'

    ### PRIVATE METHODS ###

    def _change(self, directory):
        return abjad.TemporaryDirectoryChange(directory=directory)

    def _check_test_scores_directory(self, check=False):
        if not check:
            return
        directory = self.io_manager.configuration.test_scores_directory
        names = [_.name for _ in directory.iterdir()]
        if 'red_score' not in names:
            message = f'Empty test scores directory {directory} ...'
            raise Exception(message)

    def _cleanup(self, remove=None):
        return abjad.FilesystemState(remove=remove)

    def _confirm(self, message='ok?'):
        result = self._getter(message)
        if isinstance(result, str):
            if result == '':
                return False
            if 'yes'.startswith(result.lower()):
                return True
            if 'no'.startswith(result.lower()):
                return False

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
            self._display(f'removing {target.trim()} ...')
        self._display(f'writing {target.trim()} ...')
        directory.copy_boilerplate(
            source_name=source_name,
            target_name=target_name,
            values=values,
            )

    def _display(self, lines, caps=True, is_menu=False):
        self.io_manager._display(
            lines,
            caps=caps,
            is_menu=is_menu,
            )

    def _display_errors(self, lines):
        self.io_manager._display_errors(lines)

    def _get_command_dictionary(self):
        result = {}
        methods = self._get_commands()
        for method in methods:
            result[method.command_name] = method
        return result

    def _get_commands(self):
        result = []
        for name in dir(self):
            if name.startswith('_'):
                continue
            command = getattr(self, name)
            if not inspect.ismethod(command):
                continue
            result.append(command)
        return result

    def _get_composer_tools_package_path(self):
        name = abjad.abjad_configuration.composer_library
        if not name:
            return
        try:
            path = importlib.import_module(name)
        except ImportError:
            path = None
        if not path:
            return
        path = self.Path(path.__path__[0]) / 'tools'
        return path

    def _get_scores_directory(self):
        if (self.io_manager._is_test or 
            self.io_manager._is_example):
            return self.io_manager.configuration.test_scores_directory
        return self.io_manager.configuration.composer_scores_directory

    def _getter(self, message):
        string = self.io_manager._get_input(message)
        if string == '<return>':
            return
        if string == 'q':
            self.io_manager._is_quitting = True
            return
        return string

    def _interaction(self):
        import ide
        return ide.Interaction(io_manager=self.io_manager)

    def _interpret_tex_file(self, tex):
        if not tex.is_file():
            self._display(f'can not find {tex.trim()} ...')
            return
        pdf = tex.with_suffix('.pdf')
        if pdf.exists():
            self._display(f'removing {pdf.trim()} ...')
            pdf.unlink()
        self._display(f'interpreting {tex.trim()} ...')
        self.io_manager.interpret_tex_file(tex)
        if pdf.is_file():
            self._display(f'writing {pdf.trim()} ...')
        else:
            self._display('ERROR IN LATEX LOG FILE ...')
            log_file = self.io_manager.configuration.latex_log_file_path
            with log_file.open() as file_pointer:
                lines = [_.strip('\n') for _ in file_pointer.readlines()]
            self._display(lines)

    def _make_build_directory(self, builds):
        name = self._getter('build name')
        if not name:
            return
        name = name.lower()
        name = name.replace(' ', '-')
        name = name.replace('_', '-')
        build = builds / name
        if build.exists():
            self._display(f'path already exists: {build.trim()}.')
            return
        paper_size = self._getter('paper size (ex: letter landscape)')
        if not paper_size:
            return
        orientation = 'portrait'
        if paper_size.endswith(' landscape'):
            orientation = 'landscape'
            length = len(' landscape')
            paper_size = paper_size[:-length]
        elif paper_size.endswith(' portrait'):
            length = len(' portrait')
            paper_size = paper_size[:-length]
        price = self._getter('price (ex: \$80 / \euro 72')
        suffix = self._getter('catalog number suffix (ex: ann.)')
        file_names = (
            'back-cover.tex',
            'front-cover.tex',
            'music.ly',
            'preface.tex',
            'score.tex',
            'stylesheet.ily',
            )
        file_paths = [build / _ for _ in file_names]
        self._display('making ...')
        self._display(f'   {build.trim()}')
        for file_path in file_paths:
            self._display(f'   {file_path.trim()}')
        if not self._confirm():
            return
        if build.exists():
            shutil.rmtree(str(build))
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

    def _make_command_menu_sections(self, directory, menu):
        commands = []
        for command in self._get_commands():
            if directory.is_external() and command.external:
                commands.append(command)
            elif directory.is_scores() and command.scores:
                commands.append(command)
            elif (directory.is_package_path() and
                directory.matches_manifest(command.directories) and
                not directory.matches_manifest(command.blacklist)):
                commands.append(command)
        command_groups = {}
        for command in commands:
            if command.section not in command_groups:
                command_groups[command.section] = []
            command_group = command_groups[command.section]
            command_group.append(command)
        for menu_section_name in command_groups:
            command_group = command_groups[menu_section_name]
            is_hidden = not menu_section_name == 'basic'
            menu.make_command_section(
                is_hidden=is_hidden,
                commands=command_group,
                name=menu_section_name,
                )

    def _make_file(self, directory):
        assert directory.is_dir()
        file_name = self._getter('file name')
        if file_name in (None, ''):
            return
        if not directory.is_external():
            file_name = directory._coerce_asset_name(file_name)
            name_predicate = directory.get_name_predicate()
            if not name_predicate(abjad.String(file_name)):
                self._display(f'invalid file name: {file_name!r}.')
                return
        file_path = directory / file_name
        boilerplate = self.io_manager.configuration.boilerplate_directory
        if directory.is_tools():
            if abjad.String(file_name).is_classfile_name():
                source_file = boilerplate / 'Maker.py'
                shutil.copyfile(str(source_file), str(file_path))
                template = file_path.read_text()
                class_name = file_path.stem
                completed_template = template.format(class_name=class_name)
                file_path.write_text(completed_template)
            else:
                source_file = boilerplate / 'make_something.py'
                shutil.copyfile(str(source_file), str(file_path))
                template = file_path.read_text()
                function_name = file_path.stem
                completed_template = template.format(
                    function_name=function_name,
                    )
                file_path.write_text(completed_template)
        else:
            contents = ''
            self.io_manager.write(file_path, contents)
        self.io_manager.edit(file_path)

    def _make_main_menu(self, directory):
        name = 'Abjad IDE'
        menu = directory.make_menu(io_manager=self.io_manager, name=name)
        self._make_command_menu_sections(directory, menu)
        return menu

    def _make_material_ly(self, directory):
        assert directory.is_dir()
        directory = self.Path(directory)
        assert directory.parent.name == 'materials'
        definition = directory / 'definition.py'
        if not definition.is_file():
            self._display(f'can not find {definition.trim()} ...')
            return
        source = directory / '__illustrate__.py'
        if not source.is_file():
            self._display(f'can not find {source.trim()} ...')
            return
        target = directory / 'illustration.ly'
        if target.exists():
            self._display(f'removing {target.trim()} ...')
        source_make = self.Path('boilerplate')
        source_make /= '__make_material_ly__.py'
        target_make = directory / '__make_material_ly__.py'
        with self._cleanup([target_make]):
            target_make.remove()
            shutil.copyfile(str(source_make), str(target_make))
            self._display(f'interpreting {source.trim()} ...')
            result = self.io_manager.interpret_file(str(target_make))
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.ndisplay_errors(stderr_lines)
                return
            if not target.is_file():
                self._display(f'could not make {target.trim()}.')
                return
            self._display(f'writing {target.trim()} ...')

    def _make_material_pdf(self, directory, open_after=True):
        assert directory.is_material()
        illustrate = directory / '__illustrate__.py'
        if not illustrate.is_file():
            self._display(f'can not find {illustrate.trim()} ...')
            return 0 
        definition = directory / 'definition.py'
        if not definition.is_file():
            self._display(f'can not find {definition.trim()} ...')
            return 0 
        self._display('making PDF ...')
        source = directory / 'illustration.ly'
        target = source.with_suffix('.pdf')
        boilerplate = self.Path('boilerplate')
        source_make = boilerplate / '__make_material_pdf__.py'
        target_make = directory / '__make_material_pdf__.py'
        with self._cleanup([target_make]):
            for path in (source, target):
                if path.exists():
                    self._display(f'removing {path.trim()} ...')
                    path.remove()
            shutil.copyfile(str(source_make), str(target_make))
            self._display(f'interpreting {illustrate.trim()} ...')
            result = self.io_manager.interpret_file(target_make)
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self._display_errors(stderr_lines)
            if open_after:
                self._display(f'opening {target.trim()} ...')
                self.io_manager.open_file(str(target))
            return exit_code

    def _make_score_package(self):
        scores = self.io_manager.configuration.composer_scores_directory
        if (self.io_manager._is_test or
            self.io_manager._is_example):
            scores = self.io_manager.configuration.test_scores_directory
        scores = self.Path(scores)
        wrapper = None
        for wrapper in scores._find_empty_wrappers():
            self._display(f'found {wrapper}.')
            if not self._confirm(f'populate {wrapper}?'):
                return
        title = self._getter('enter title')
        if not title:
            return
        if not wrapper:
            name = abjad.String(title).strip_diacritics()
            name = abjad.String(name).to_snake_case()
            wrapper = scores / name
            if wrapper.exists():
                self._display(f'directory already exists: {wrapper}.')
                return
        self._display(f'making {wrapper} ...')
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
        scores.add_metadatum('view', None)

    def _make_segment_ly(self, directory):
        assert directory.is_segment()
        definition = directory / 'definition.py'
        if not definition.is_file():
            self._display(f'can not find {definition.trim()} ...')
            return
        directory.update_order_dependent_segment_metadata()
        boilerplate = self.io_manager.configuration.boilerplate_directory
        source_make = boilerplate / '__make_segment_ly__.py'
        target_make = directory / '__make_segment_ly__.py'
        target_make.remove()
        with self._cleanup([target_make]):
            source = directory / '__illustrate__.py'
            target = directory / 'illustration.ly'
            if target.exists():
                self._display(f'removing {target.trim()} ...')
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
                self._display(f'removing {source.trim()} ...')
                self._display(f'writing {source.trim()} ...')
            self._display(f'interpreting {source.trim()} ...')
            result = self.io_manager.interpret_file(target_make)
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self._display_errors(stderr_lines)
                return
            self._display(f'writing {target.trim()} ...')

    def _make_segment_midi(self, directory, open_after=True):
        assert directory.is_segment()
        definition_path = directory / 'definition.py'
        if not definition_path.is_file():
            self._display(f'can not find {definition_path.trim()} ...')
            return -1
        self._display('making MIDI ...')
        directory.update_order_dependent_segment_metadata()
        boilerplate = self.io_manager.configuration.boilerplate_directory
        boilerplate /= '__make_segment_midi__.py'
        maker = directory / '__midi__.py'
        ly = directory / 'midi.ly'
        midi = directory / 'segment.midi'
        for path in (ly, midi):
            if path.exists():
                self._display(f'removing {path.trim()} ...')
                path.unlink()
        if maker.exists():
            self._display(f'removing {maker.trim()} ...')
            maker.unlink()
        self._display(f'writing {maker.trim()} ...')
        self._display(f'interpreting {maker.trim()} ...')
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
        result = self.io_manager.interpret_file(maker)
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self._display_errors(stderr_lines)
            return exit_code
        log = abjad.abjad_configuration.lilypond_log_file_path
        log = self.Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                self._display('ERROR IN LILYPOND LOG FILE ...')
                break
        if midi.is_file() and open_after:
            self._open_file(midi)
        return 0

    def _make_segment_pdf(self, directory, open_after=True):
        assert directory.is_segment()
        definition_path = directory / 'definition.py'
        if not definition_path.is_file():
            self._display(f'can not find {definition_path.trim()} ...')
            return -1
        self._display('making PDF ...')
        directory.update_order_dependent_segment_metadata()
        boilerplate = self.io_manager.configuration.boilerplate_directory
        boilerplate_path = boilerplate / '__illustrate_segment__.py'
        illustrate = directory / '__illustrate__.py'
        ly = directory / 'illustration.ly'
        pdf = directory / 'illustration.pdf'
        for path in (ly, pdf):
            if path.exists():
                self._display(f'removing {path.trim()} ...')
                path.unlink()
        if illustrate.exists():
            self._display(f'removing {illustrate.trim()} ...')
            illustrate.unlink()
        self._display(f'writing {illustrate.trim()} ...')
        self._display(f'interpreting {illustrate.trim()} ...')
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
        result = self.io_manager.interpret_file(illustrate)
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self._display_errors(stderr_lines)
            return exit_code
        log = abjad.abjad_configuration.lilypond_log_file_path
        log = self.Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                self._display('ERROR IN LILYPOND LOG FILE ...')
                break
        if pdf.is_file() and open_after:
            self._open_file(pdf)
        return 0

    def _make_selector(self, header=None, items=None):
        import ide
        menu = ide.Menu(
            break_on_return=True,
            header=header,
            io_manager=self._io_manager,
            name='selector',
            )
        menu_entries = []
        for item in items:
            assert isinstance(item, str), repr(item)
            menu_entries.append((item, None, None, item))
        if not menu_entries:
            return menu
        menu._make_section(
            is_asset_section=True,
            is_numbered=True,
            menu_entries=menu_entries,
            name='assets',
            return_value_attribute='explicit',
            )
        return menu

    def _manage_directory(self, directory):
        import ide
        if not directory.exists():
            self._display(f'missing {directory.trim()} ...')
            return
        if not self._current_directory == directory:
            self._previous_directory = self._current_directory
            self._current_directory = directory
        self._io_manager._is_redrawing = True
        while True:
            if self.io_manager._is_quitting:
                return
            if not self._current_directory == directory:
                self._previous_directory = self._current_directory
                self._current_directory = directory
            menu = self._make_main_menu(directory)
            response = menu()
            with self._interaction():
                if self.io_manager._is_quitting:
                    return
                elif response.string.startswith('!'):
                    with self._change(directory):
                        self.io_manager._invoke_shell(response.string[1:])
                elif response.string[0] in self._addressing_characters:
                    path = directory.match_package_path(response.string[1:])
                    if path is None:
                        message = f'matches no path {response.string!r} ...'
                        self._display(message)
                    elif response.string[0] == '@':
                        if path.is_package():
                            path = path / 'definition.py'
                        self._open_file(path)
                    elif response.string[0] == '%':
                        self._manage_directory(path)
                    elif response.string[0] == '^':
                        self._run_doctest(path)
                    elif response.string[0] == '*':
                        if path.is_package():
                            path /= 'illustration.pdf'
                        self._open_file(path)
                elif (response.known and
                    response.payload in self._get_command_dictionary()):
                    command = self._get_command_dictionary()[response.payload]
                    if command.argument_name == 'directory':
                        command(self._current_directory)
                    else:
                        command()
                elif (isinstance(response.payload, ide.Path) or
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
                        self._manage_directory(path)
                    else:
                        self._display(f'missing {path.trim()} ...')
                else:
                    assert response.payload is None
                    self._display(f'unknown command {response.string!r} ...')
                    if self.io_manager._is_test:
                        raise Exception(response)

    def _match_alias(self, directory, string):
        if not self.io_manager.configuration.aliases:
            return
        if not self.io_manager.configuration.aliases.get(string):
            return
        value = self.io_manager.configuration.aliases.get(string)
        path = self.Path(value)
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
        string = self.Path._smart_match(strings, argument)
        if string is not None:
            return paths[strings.index(string)]

    def _menu_entry(self, display_string, explicit_return_value):
        from ide.tools.idetools.MenuEntry import MenuEntry
        return MenuEntry(
            display_string=display_string,
            explicit_return_value=explicit_return_value,
            )

    def _open_every_file(self, paths):
        for path in paths:
            if path.suffix in self.io_manager._editor_extensions:
                self._display(f'editing {path.trim()} ...')
            else:
                self._display(f'opening {path.trim()} ...')
        self.io_manager.open_file(paths)

    def _open_file(self, file_path):
        if file_path.is_file():
            if file_path.suffix in self.io_manager._editor_extensions:
                self._display(f'editing {file_path.trim()} ...')
            else:
                self._display(f'opening {file_path.trim()} ...')
            if not self.io_manager._is_test:
                self.io_manager.open_file(file_path)
        else:
            self._display(f'missing {file_path.trim()} ...')

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

    def _run_doctest(self, path):
        assert path.exists()
        self._display(f'running doctest on {path.trim()} ...')
        command = f'ajv doctest -x {path}'
        self.io_manager.spawn_subprocess(command)

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
        with self._change(directory), self._cleanup([backup_pdf]):
            if pdf.exists():
                self._display(f'removing {pdf.trim()} ...')
                shutil.move(str(pdf), str(backup_pdf))
                assert not pdf.exists()
            else:
                backup_pdf = None
            self._display(f'interpreting {ly.trim()} ...')
            abjad.IOManager.run_lilypond(str(ly))
            if not pdf.is_file():
                self._display(f'can not produce {pdf.trim()} ...')
                if backup_pdf:
                    self._display(f'restoring {backup_pdf.trim()} ...')
                    shutil.move(str(backup_pdf), str(pdf))
            self._display(f'writing {pdf.trim()} ...')

    def _run_pytest(self, path):
        assert path.exists()
        self._display(f'running pytest on {path.trim()} ...')
        command = f'py.test -xrf {path}'
        self.io_manager.spawn_subprocess(command)

    def _select_available_path(self, directory):
        assert directory.is_dir()
        asset_type = directory.get_asset_type()
        while True:
            default_prompt = f'enter {asset_type} name'
            name = self._getter(default_prompt)
            if not name:
                return
            name = abjad.String(name).strip_diacritics()
            words = abjad.String(name).delimit_words()
            words = [_.lower() for _ in words]
            name = '_'.join(words)
            if not abjad.String(name).is_snake_case_package_name():
                continue
            path = directory / name
            if path.exists():
                self._display(f'path already exists: {path!r}.')
            else:
                return path

    def _select_path(self, directory, infinitive_phrase=None):
        paths = directory.list_paths()
        if not paths:
            message = 'no paths'
            if infinitive_phrase is not None:
                message = message + ' ' + infinitive_phrase
            message = message + '.'
            self._display(message)
            return
        asset_type = directory.get_asset_type()
        message = f'enter {asset_type}'
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        result = self._getter(message)
        if not result:
            return
        path = self._match_path(paths, result)
        if path is None:
            self._display(f'matches no path {result!r} ...')
        return path

    def _select_path_to_copy(self, directory, score=None):
        directories = directory._collect_in_every_score()
        if score:
            filter_ = str(score.contents)
        else:
            filter_ = str(directory.contents)
        directories = [_ for _ in directories if str(_).startswith(filter_)]
        paths = []
        for directory_ in directories:
            for path in directory_.glob('*'):
                if path.name[0].isalpha():
                    paths.append(path.trim())
        header = directory.get_header()
        header = header + ' - select path to copy:'
        menu = self._make_selector(items=paths, header=header)
        self._io_manager._is_redrawing = True
        response = menu()
        path = None
        if response.payload in paths:
            path = response.payload
        elif not response.known:
            scores = self._get_scores_directory()
            for score in scores.iterdir():
                if response.string == score.name:
                    path = self._select_path_to_copy(directory, score=score)
        if not path:
            return
        path = type(directory)(path)
        scores = self._get_scores_directory()
        path = scores / path.parts[0] / path
        return path

    def _select_paths(self, directory, infinitive_phrase=None):
        paths = directory.list_paths()
        if not paths:
            message = 'no paths'
            if infinitive_phrase is not None:
                message = message + ' ' + infinitive_phrase
            message = message + '.'
            self._display(message)
            return
        asset_type = directory.get_asset_type()
        message = f'enter {asset_type}(s)'
        if infinitive_phrase is not None:
            message += ' ' + infinitive_phrase
        result = self._getter(message)
        if not result:
            return
        if isinstance(result, int):
            result = [result]
        elif isinstance(result, str) and ',' in result:
            result_ = result.split(',')
            result = []
            for part in result_:
                part = part.strip()
                if abjad.mathtools.is_integer_equivalent(part):
                    part = int(part)
                result.append(part)
        elif isinstance(result, str) and ',' not in result:
            result = [result]
        paths_ = []
        for string in result:
            path = self._match_path(paths, string)
            if path is None:
                self._display(f'matches no path {string!r} ...')
            else:
                paths_.append(path)
        return paths_

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
            self._display(f'trashing {path.trim()} ...')
            path.unlink()
        else:
            self._display(f'missing {path.trim()} ...')

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
    def io_manager(self):
        r'''Gets IO manager.

        Returns IO manager.
        '''
        return self._io_manager

    @property
    def Path(self):
        r'''Gets IDE path class.

        Returns IDE path class.
        '''
        import ide
        return ide.Path

    ### PUBLIC METHODS ###

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
        self._display('building score ...')
        self.collect_segment_lys(directory)
        self.generate_music(directory)
        self.interpret_music(directory, open_after=False)
        tex = directory / 'front-cover.tex'
        pdf = directory / 'front-cover.pdf'
        if tex.is_file():
            self.interpret_front_cover(directory, open_after=False)
        elif pdf.is_file():
            self._display(f'using existing {pdf.trim()} ...')
        else:
            self._display('missing front cover ...')
            return
        tex = directory / 'preface.tex'
        pdf = directory / 'preface.pdf'
        if tex.is_file():
            self.interpret_preface(directory, open_after=False)
        elif pdf:
            self._display(f'using existing {pdf.trim()} ...')
        else:
            self._display('missing preface ...')
            return
        tex = directory / 'back-cover.tex'
        pdf = directory / 'back-cover.pdf'
        if tex.is_file():
            self.interpret_back_cover(directory, open_after=False)
        elif pdf.is_file():
            self._display(f'using existing {pdf.trim()} ...')
        else:
            self._display('missing back cover ...')
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
        self._display('checking definition file ...')
        definition = directory / 'definition.py'
        if not definition.is_file():
            self._display(f'missing {definition.trim()} ...')
            return
        with abjad.Timer() as timer:
            result = self.io_manager.interpret_file(definition)
        stdout_lines, stderr_lines, exit_code = result
        self._display(stdout_lines)
        if exit_code:
            self._display([f'{definition.trim()} FAILED:'] + stderr_lines)
        else:
            self._display(f'{definition.trim()} ... OK', caps=False)
        self._display(timer.total_time_message)
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
        self._display('collecting segment lys ...')
        pairs = directory._collect_segment_lys()
        if not pairs:
            self._display('... no segment lys found.')
            return
        if not directory._segments.is_dir():
            _segments_directory.mkdir()
        for source, target in pairs:
            if target.exists():
                self._display(f'removing {target.trim()} ...')
            self._display(f'writing {target.trim()} ...')
            text = self._trim_ly(source)
            target.write_text(text)

    @Command(
        'cp',
        argument_name='directory',
        blacklist=('contents',),
        directories=True,
        scores=True,
        section='basic',
        )
    def copy(self, directory):
        r'''Copies into `directory`.

        Returns none.
        '''
        source = self._select_path_to_copy(directory)
        if not source:
            return
        target = directory / source.name
        if source == target:
            self._display(f'existing {target.trim()} ...')
            name = self._getter('enter new name')
            if not name:
                return
            target = target.with_name(name)
        if source == target:
            return
        if source.is_file():
            shutil.copyfile(str(source), str(target))
        elif source.is_dir():
            shutil.copytree(str(source), str(target))
        else:
            raise ValueError(source)
        self._display(f'writing {target.trim()} ...')

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
        self._open_file(self.io_manager.configuration.aliases_file_path)
        self.io_manager.configuration._read_aliases_file()

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
        with self._interaction():
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
        'ee*',
        argument_name='directory',
        description='every string - edit',
        directories=True,
        external=True,
        scores=True,
        section='star',
        )
    def edit_every(self, directory):
        r'''Opens Vim and goes to every occurrence of search string.

        Returns none.
        '''
        search_string = self._getter('enter search string')
        if not search_string:
            return
        command = rf'vim -c "grep {search_string!s} --type=python"'
        if self.io_manager._is_test:
            return
        with self._change(directory):
            self.io_manager.spawn_subprocess(command)

    @Command(
        'df*',
        argument_name='directory',
        description='every definition file - edit',
        directories=('materials', 'segments'),
        section='star',
        )
    def edit_every_definition_file(self, directory):
        r'''Edits definition file in every subdirectory of `directory`.

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
        r'''Edits files in every subdirectory of `directory`.

        Returns none.
        '''
        import ide
        name = self._getter('enter filename')
        if not name:
            return
        command = f'find {directory!s} -name {name}'
        paths = self.io_manager.run_command(command)
        if not paths:
            self._display(f'missing {name!r} files ...')
        else:
            paths = [ide.Path(_) for _ in paths]
            self._open_every_file(paths)

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
        self._open_file(self.io_manager.configuration.latex_log_file_path)

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
        self._open_file(self.Path(target))

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
        'pe',
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
        self._display('generating back cover ...')
        values = {}
        contents = directory.contents
        catalog_number = contents.get_metadatum('catalog_number')
        name = 'catalog_number_suffix'
        catalog_number_suffix = contents.get_metadatum(name)
        if catalog_number_suffix:
            catalog_number += f' / {catalog_number_suffix}'
        values['catalog_number'] = catalog_number
        composer_website = abjad.abjad_configuration.composer_website or ''
        if self.io_manager._is_test or self.io_manager._is_example:
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
        self._display('generating subdirectory stylesheet ...')
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
            'build-subdirectory-stylesheet.ily',
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
        self._display('generating front cover ...')
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
        if (self.io_manager._is_test or
            self.io_manager._is_example):
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
        self._display('generating music ...')
        target = directory / 'music.ly'
        if target.exists():
            self._display(f'removing {target.trim()} ...')
            target.unlink()
        paths = contents.segments.list_paths()
        if paths:
            view = contents.segments.get_metadatum('view')
            if bool(view):
                self._display(f'examining segments in view order ...')
            else:
                self._display('examining segments alphabetically ...')
        else:
            self._display('no segments found ...')
        for path in paths:
            self._display(f'examining {path.trim()} ...')
        names = [_.stem.replace('_', '-') for _ in paths]
        source = self.Path('boilerplate') / 'music.ly'
        self._display(f'writing {target.trim()} ...')
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
        'pg',
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
        self._display('generating preface ...')
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
        self._display('generating score ...')
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
        if not directory._is_in_git_repository():
            self._display(f'missing {directory.trim()} repository ...')
            return
        with self._change(directory.wrapper):
            self._display(f'git commit {directory.wrapper} ...')
            if not directory.wrapper._has_pending_commit():
                self._display(f'{directory.wrapper} ... nothing to commit.')
                return
            self.io_manager.spawn_subprocess('git status .')
            if self.io_manager._is_test:
                return
            command = f'git add -A {directory.wrapper}'
            lines = self.io_manager.run_command(command)
            self._display(lines, caps=False)
            if commit_message is None:
                commit_message = self._getter('commit message')
                if not commit_message:
                    return
            command = f'git commit -m "{commit_message}" {directory.wrapper}'
            command += '; git push'
            lines = self.io_manager.run_command(command)
            self._display(lines, caps=False)

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
        commit_message = self._getter('commit message')
        if not commit_message:
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
        if not directory._is_in_git_repository():
            self._display(f'missing {directory.trim()} repository ...')
            return
        with self._change(directory):
            self.io_manager.spawn_subprocess(f'git diff {directory}')

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
        if not directory._is_in_git_repository():
            self._display(f'missing {directory.trim()} repository ...')
            return
        with self._change(directory.wrapper):
            self._display(f'git pull {directory.wrapper} ...')
            if not self.io_manager._is_test:
                lines = self.io_manager.run_command('git pull .')
                if lines and 'Already up-to-date' in lines[-1]:
                    lines = lines[-1:]
                self._display(lines)
                command = 'git submodule foreach git pull origin master'
                self._display(f'{command} ...')
                lines = self.io_manager.run_command(command)
                if lines and 'Already up-to-date' in lines[-1]:
                    lines = lines[-1:]
                self._display(lines)

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
        if not directory._is_in_git_repository():
            self._display(f'missing {directory.trim()} repository ...')
            return
        with self._change(directory.wrapper):
            self._display(f'git push {directory.wrapper} ...')
            if not self.io_manager._is_test:
                self.io_manager.spawn_subprocess('git push .')

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
        if not directory._is_in_git_repository():
            self._display(f'missing {directory.trim()} repository ...')
            return
        with self._change(directory.wrapper):
            self._display(f'git status {directory.wrapper} ...')
            self.io_manager.spawn_subprocess('git status .')
            self._display('')
            command = 'git submodule foreach git fetch'
            self._display(f'{command} ...')
            self.io_manager.spawn_subprocess(command)

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
        if self._previous_directory:
            self._manage_directory(self._previous_directory)

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
    def go_to_builds_directory_segments(self, directory):
        r'''Goes to _segments directory.

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
        directory = self.io_manager.configuration.composer_scores_directory
        if (self.io_manager._is_test or
            self.io_manager._is_example):
            directory = self.io_manager.configuration.test_scores_directory
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
        self._display('interpreting back cover ...')
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
        self._display('interpreting every ly ...')
        paths = directory.list_paths()
        sources = []
        for path in paths:
            source = path / 'illustration.ly'
            if source.is_file():
                sources.append(source)
        if not sources:
            self._display('no LilyPond files found.')
            return
        with abjad.Timer() as timer:
            for source in sources:
                self.interpret_ly(source.parent, open_after=False)
            self._display(timer.total_time_message)

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
        self._display('interpreting front cover ...')
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
        self._display('interpreting ly ...')
        source = directory / 'illustration.ly'
        target = source.with_suffix('.pdf')
        if source.is_file():
            self._run_lilypond(source)
        else:
            self._display(f'missing {source.trim()} ...')
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
        self._display('interpreting music ...')
        source = directory / 'music.ly'
        target = source.with_suffix('.pdf')
        if not source.is_file():
            self._display(f'can not find {source.trim()} ...')
            return
        self._run_lilypond(source)
        if target.is_file() and open_after:
            self._open_file(target)

    @Command(
        'pi',
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
        self._display('interpreting preface ...')
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
        self._display('interpreting score ...')
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
        'kp',
        argument_name='directory',
        directories=('tools',),
        section='scripts',
        )
    def keep(self, directory):
        r'''Pushes tools file to composer library for safe-keeping.

        Returns none.
        '''
        assert directory.is_package_path()
        source = self._select_path_to_copy(directory)
        if not source:
            return
        target = self._get_composer_tools_package_path()
        if not target.is_dir():
            self._display(f'missing {target} ...')
            return
        target = target / source.name
        if target.exists():
            self._display(f'existing {target.trim()} ...')
            return
        if source.is_file():
            shutil.copyfile(str(source), str(target))
        elif source.is_dir():
            shutil.copytree(str(source), str(target))
        else:
            raise ValueError(source)
        self._display(f'writing {target.trim()} ...')

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
        source = self.Path('boilerplate')
        source /= '__illustrate_material__.py'
        target = directory / '__illustrate__.py'
        if target.is_file():
            self._display(f'preserving {target.trim()} ...')
            return
        self._display(f'writing {target.trim()} ...')
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
        self._display('making ly ...')
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
        r'''Makes new asset.

        Returns none.
        '''
        if directory.is_scores():
            self._make_score_package()
        elif directory.is_package_path(('materials', 'segments')):
            path = self._select_available_path(directory)
            if path:
                path._make_package()
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
                if str(path).endswith('.pdf'):
                    pdfs.append(path)
                elif path.is_dir():
                    for pdf_ in path.glob('*.pdf'):
                        pdfs.append(pdf_)
        if not pdfs:
            self._display('missing PDFs ...')
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
        'po',
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
            self._display(message)

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
        'spp',
        argument_name='directory',
        description='score pdf - publish',
        directories=('build',),
        section='builds',
        )
    def publish_score_pdf(self, directory):
        r'''Publishes score PDF in distribution directory.

        Returns none.
        '''
        assert directory.is_build()
        self._display('publishing score PDF ...')
        source = directory / 'score.pdf'
        if not source.exists():
            self._display(f'missing {source.trim()} ...')
            return
        name = directory.contents.name
        name = name.replace('_', '-')
        if name.endswith('-score'):
            name = f'{name}.pdf'
        else:
            name = f'{name}-score.pdf'
        target = directory.distribution / name
        self._display(f' FROM: {source.trim()}')
        self._display(f'   TO: {target.trim()}')
        shutil.copyfile(str(source), str(target))

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
        self.io_manager._is_quitting = True

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
        paths = self._select_paths(directory, 'to remove')
        if not paths:
            return
        count = len(paths)
        if count == 1:
            if paths[0].is_contents():
                path_ = paths[0].wrapper
            else:
                path_ = paths[0]
            self._display(f'confirming {path_.trim()} ...')
        else:
            self._display('confirming ...')
            for path in paths:
                if path.is_contents():
                    path_ = path.wrapper
                else:
                    path_ = path
                self._display(f'    {path_.trim()}')
        if count == 1:
            confirmation_string = 'remove'
        else:
            confirmation_string = f'remove {count}'
        result = self._getter(f"type {confirmation_string!r} to proceed")
        if result is None:
            return
        if not result == confirmation_string:
            return
        for path in paths:
            if path.is_contents():
                path = path.wrapper
            if path._is_in_git_repository():
                if path._is_git_unknown():
                    command = f'rm -rf {path}'
                else:
                    command = f'git rm --force -r {path}'
            else:
                command = f'rm -rf {path}'
            with self._change(path.parent):
                self._display(f'removing {path.trim()} ...')
                self.io_manager.run_command(command)
            executables = self.io_manager.find_executable('trash')
            executables = [self.Path(_) for _ in executables]
            if executables and executables[0].is_file():
                executable = executables[0]
                cleanup_command = str(executable) + f' {path}'
            else:
                cleanup_command = f'rm -rf {path}'
            self.io_manager.run_command(cleanup_command)

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
        source = self._select_path(directory, 'to rename')
        if not source:
            return
        if source.is_contents():
            source = source.parent
        self._display(f'renaming {source.trim()} ...')
        target = self._getter('new name')
        if not target:
            return
        original_target_name = target
        target = directory._coerce_asset_name(target)
        target = source.parent / target
        if target.exists():
            self._display(f'existing {target.trim()!r} ...')
            return
        self._display('Renaming ...')
        self._display(f' FROM: {source.trim()}')
        self._display(f'   TO: {target.trim()}')
        if not self._confirm():
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
        r'''Replaces expression.

        Returns none.
        '''
        search_string = self._getter('enter search string')
        if not search_string:
            return
        replace_string = self._getter('enter replace string')
        if not replace_string:
            return
        complete_words = False
        result = self._confirm('complete words only?')
        if result:
            complete_words = True
        command = f'ajv replace {search_string!r} {replace_string!r} -Y'
        if complete_words:
            command += ' -W'
        if directory == directory.scores:
            pass
        else:
            directory = directory.wrapper
        with self._change(directory):
            lines = self.io_manager.run_command(command)
            lines = [_.strip() for _ in lines if not _ == '']
            self._display(lines, caps=False)

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
        with self._change(directory):
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
        with self._change(directory):
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
        executables = self.io_manager.find_executable('ack')
        if not executables:
            executables = self.io_manager.find_executable('grep')
        executables = [self.Path(_) for _ in executables]
        if not executables:
            self._display('can not find ack.')
            self._display('can not find grep.')
            return
        assert 1 <= len(executables)
        executable = None
        for path in executables:
            if path.is_file():
                executable = path
        if executable is None:
            self._display('can not find ack.')
            self._display('can not find grep.')
            return
        search_string = self._getter('enter search string')
        if not search_string:
            return
        if executable.name == 'ack':
            command = r'{!s} --ignore-dir=_docs {} --type=python'
            command = command.format(executable, search_string)
        elif executable.name == 'grep':
            command = rf'{executable!s} -r {search_string!r} *'
        if directory.wrapper is not None:
            directory = directory.wrapper
        with self._change(directory):
            lines = self.io_manager.run_command(command)
            self._display(lines, caps=False)

    @Command(
        'illt',
        argument_name='directory',
        description='illustrate file - trash',
        directories=('material',),
        section='illustrate_file',
        )
    def trash_illustrate(self, directory):
        r'''Trashes illustration file.

        Returns none.
        '''
        assert directory.is_material()
        self._trash_file(directory / '__illustrate__.py')

    @Command(
        'lyt',
        argument_name='directory',
        description='ly - trash',
        directories=('material', 'segment',),
        section='ly',
        )
    def trash_ly(self, directory):
        r'''Trashes illustration LilyPond file.

        Returns none.
        '''
        assert directory.is_package()
        self._trash_file(directory / 'illustration.ly')

    @Command(
        'trash',
        argument_name='directory',
        description='ly & pdf - trash',
        directories=('material', 'segment',),
        section='ly & pdf',
        )
    def trash_ly_and_pdf(self, directory):
        r'''Trashes illustration LilyPond file and illustration PDF.

        Returns none.
        '''
        assert directory.is_package()
        self._trash_file(directory / 'illustration.ly')
        self._trash_file(directory / 'illustration.pdf')

    @Command(
        'pdft',
        argument_name='directory',
        description='pdf - trash',
        directories=('material', 'segment',),
        section='pdf',
        )
    def trash_pdf(self, directory):
        r'''Trashes illustration PDF.

        Returns none.
        '''
        assert directory.is_package()
        self._trash_file(directory / 'illustration.pdf')
