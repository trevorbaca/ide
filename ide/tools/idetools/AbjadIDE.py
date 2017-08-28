from __future__ import print_function
import abjad
import datetime
import inspect
import os
import pathlib
import shutil
import sys
import traceback
from ide.tools.idetools.Command import Command


class AbjadIDE(object):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> abjad_ide = ide.AbjadIDE()
            >>> abjad_ide
            AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_io_manager',
        '_session',
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

    _secondary_names = (
        '__illustrate__.py',
        '__init__.py',
        '__metadata__.py',
        '__views__.py',
        '_segments',
        )

    _tab = 4 * ' '

    ### INITIALIZER ###

    def __init__(self, session=None, is_example=False, is_test=False):
        from ide.tools.idetools.Configuration import Configuration
        from ide.tools.idetools.IOManager import IOManager
        from ide.tools.idetools.Session import Session
        self._configuration = Configuration()
        if session is None:
            session = Session()
            session._is_example = is_example
            session._is_test = is_test
        self._session = session
        self._io_manager = IOManager(session=session)

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of AbjadIDE.

        Returns string.
        '''
        return f'{type(self).__name__}()'

    ### PRIVATE METHODS ###

    def _collect_all_display_strings(self, directory):
        assert directory.is_dir()
        strings, paths = [], []
        # ordered by priority instead of alphabetically
        names = (
            'segments',
            'materials',
            'tools',
            'build',
            'stylesheets',
            'etc',
            'distribution',
            'test',
            )
        if not self._is_score_directory(directory):
            paths_ = self._list_visible_paths(directory)
            paths.extend(paths_)
            strings_ = [self._to_menu_string(_) for _ in paths_]
            strings.extend(strings_)
        directories = []
        directories.append(directory)
        for name in names:
            directory_ = self._to_score_directory(directory, name)
            if directory_:
                directories.append(directory_)
        for directory_ in directories:
            paths_ = self._list_visible_paths(directory_)
            paths.extend(paths_)
            strings_ = [self._to_menu_string(_) for _ in paths_]
            strings.extend(strings_)
        paths = [str(_) for _ in paths]
        assert len(strings) == len(paths), repr((len(strings), len(paths)))
        return strings, paths

    def _collect_segment_lys(self, directory):
        assert directory.is_dir()
        segments_directory = self._to_score_directory(directory, 'segments')
        build_directory = self._to_score_directory(directory, 'build')
        _segments_directory = build_directory / '_segments'
        entries = sorted(segments_directory.glob('*'))
        entries = [_.name for _ in entries]
        source_ly_paths, target_ly_paths = [], []
        for entry in entries:
            segment_directory = segments_directory / entry
            if not segment_directory.is_dir():
                continue
            source_ly_path = segment_directory / 'illustration.ly'
            if not source_ly_path.is_file():
                continue
            entry = entry.replace('_', '-')
            target_ly_name = entry + '.ly'
            target_ly_path = _segments_directory / target_ly_name
            source_ly_paths.append(source_ly_path)
            target_ly_paths.append(target_ly_path)
        if not build_directory.is_dir():
            build_directory.mkdir()
        pairs = zip(source_ly_paths, target_ly_paths)
        return pairs

    def _collect_similar_directories(self, directory, example_scores=False):
        assert isinstance(directory, self.Path), repr(directory)
        assert directory.is_dir()
        if not self._is_score_directory(directory):
            return [directory]
        directories = []
        scores_directories = [self._configuration.composer_scores_directory]
        if example_scores:
            scores_directory = self._configuration.example_scores_directory
            scores_directories.append(scores_directory)
        if self._is_score_directory(directory, 'scores'):
            return scores_directories
        score_directories = []
        for scores_directory in scores_directories:
            for path in scores_directory.glob('*'):
                if not path.name[0].isalpha():
                    continue
                score_directory = scores_directory / path.name
                if not score_directory.is_dir():
                    continue
                score_directories.append(score_directory)
        if self._is_score_directory(directory, 'wrapper'):
            return score_directories
        wrapper_directories = score_directories
        score_directories = []
        for wrapper_directory in wrapper_directories:
            base_name = wrapper_directory.name
            score_directory = wrapper_directory / base_name
            if not score_directory.is_dir():
                continue
            score_directories.append(score_directory)
        if self._is_score_directory(directory, ('contents', 'score')):
            return score_directories
        if self._is_score_directory(directory, ('material', 'segment')):
            directories = []
            parent_directory = directory.parent
            parent_directories = self._collect_similar_directories(
                parent_directory,
                example_scores=example_scores,
                )
            for parent_directory in parent_directories:
                for path in parent_directory.glob('*'):
                    if not path.name[0].isalpha():
                        continue
                    directory_ = parent_directory / path.name
                    if not directory_.is_dir():
                        continue
                    directories.append(directory_)
            return directories
        if self._is_score_directory(directory, 'build subdirectory'):
            directories = []
            build_directory = directory.parent
            build_directories = self._collect_similar_directories(
                build_directory,
                example_scores=example_scores,
                )
            for build_directory in build_directories:
                for path in build_directory.glob('*'):
                    if not path.name[0].isalnum():
                        continue
                    directory_ = build_directory / path.name
                    if not directory_.is_dir():
                        continue
                    directories.append(directory_)
            return directories
        if self._is_score_directory(directory, '_segments'):
            directories = []
            build_directory = directory.parent
            build_directories = self._collect_similar_directories(
                build_directory,
                example_scores=example_scores,
                )
            for build_directory in build_directories:
                for path in build_directory.glob('*'):
                    if not path.name == '_segments':
                        continue
                    directory_ = build_directory / path.name
                    if not directory_.is_dir():
                        continue
                    directories.append(directory_)
            return directories
        base_name = directory.name
        for score_directory in score_directories:
            directory_ = score_directory / base_name
            if directory_.is_dir():
                directories.append(directory_)
        return directories

    def _configure_travis_tests(self, file_path):
        assert file_path.is_file()
        test_directory = file_path.parent
        contents_directory = test_directory.parent
        wrapper_directory = contents_directory.parent
        composer_scores_directory = wrapper_directory.parent
        directory = composer_scores_directory
        self._configuration._composer_scores_directory_override = directory
        materials_directory = self._to_score_directory(file_path, 'materials')
        material_directories = self._list_visible_paths(materials_directory)
        segments_directory = self._to_score_directory(file_path, 'segments')
        segment_directories = self._list_visible_paths(segments_directory)
        return material_directories, segment_directories

    def _copy_boilerplate(
        self,
        source_file_name,
        target_directory,
        target_file_name=None,
        replacements=None,
        ):
        assert target_directory.is_dir()
        replacements = replacements or {}
        source_path = self.Path('boilerplate') / source_file_name
        target_file_name = target_file_name or source_file_name
        target_path = target_directory / target_file_name
        suffix = source_path.suffix
        messages = []
        if target_path.exists():
            messages.append(f'removing {self._trim(target_path)} ...')
        shutil.copyfile(str(source_path), str(target_path))
        template = target_path.read_text()
        template = template.format(**replacements)
        messages.append(f'writing {self._trim(target_path)} ...')
        target_path.write_text(template)
        return messages

    def _display(self, lines, capitalize=True, is_menu=False):
        self._io_manager._display(
            lines,
            capitalize=capitalize,
            is_menu=is_menu,
            )

    @classmethod
    def _entry_point(class_):
        input_ = ' '.join(sys.argv[1:])
        abjad_ide = class_()
        abjad_ide._start(input_=input_)

    def _filter_by_view(self, directory, entries, view):
        assert directory.is_dir()
        if view is None:
            return entries
        entries = entries[:]
        filtered_entries = []
        for pattern in view:
            if ':ds:' in pattern:
                for entry in entries:
                    if self._match_display_string_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            elif 'md:' in pattern:
                pairs = []
                for entry in entries:
                    metadatum = self._match_metadata_view_pattern(
                        pattern,
                        entry,
                        )
                    if metadatum is not None:
                        pair = (metadatum, entry)
                        pairs.append(pair)
                pairs.sort(key=lambda _: _[0])
                pairs.reverse()
                entries_ = [_[-1] for _ in pairs]
                filtered_entries.extend(entries_)
            elif ':path:' in pattern:
                for entry in entries:
                    if self._match_path_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            else:
                for entry in entries:
                    display_string, _, _, path = entry
                    if pattern == display_string:
                        filtered_entries.append(entry)
        return filtered_entries

    def _find_empty_score_directories(self):
        empty_score_directories = []
        scores_directories = (
            self._configuration.composer_scores_directory,
            self._configuration.example_scores_directory,
            )
        for scores_directory in scores_directories:
            for path in scores_directory.glob('*'):
                if not path.name[0].isalpha():
                    continue
                if not path.name[0].islower():
                    continue
                score_directory = path
                if not score_directory.is_dir():
                    continue
                for path in score_directory.glob('*'):
                    if not path.name[0].isalpha():
                        continue
                    if path.is_dir():
                        break
                else:
                    score_directory = self.Path(score_directory)
                    empty_score_directories.append(score_directory)
        return empty_score_directories

    def _get_added_asset_paths(self, path):
        paths = []
        git_status_lines = self._get_git_status_lines(path)
        for line in git_status_lines:
            line = str(line)
            if line.startswith('A'):
                path = line.strip('A')
                path = path.strip()
                root_directory = self._get_repository_root_directory(path)
                path = root_directory / path
                paths.append(path)
        return paths

    def _get_available_path(self, directory):
        assert directory.is_dir()
        asset_identifier = self._to_asset_identifier(directory)
        while True:
            default_prompt = 'enter {} name'
            default_prompt = default_prompt.format(asset_identifier)
            getter = self._io_manager._make_getter()
            getter.append_string(default_prompt)
            name = getter._run(io_manager=self._io_manager)
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
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._display(line)
            else:
                return path

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
            if name == 'Path':
                continue
            command = getattr(self, name)
            if not inspect.ismethod(command):
                continue
            result.append(command)
        return result

    def _get_file_path_ending_with(self, directory, string):
        if not directory.is_dir():
            return
        glob = '*{}'.format(string)
        for path in directory.glob(glob):
            if path.is_file():
                return path

    def _get_git_status_lines(self, path):
        command = 'git status --porcelain {!s}'
        command = command.format(path)
        directory = self._to_score_directory(path, 'wrapper')
        with abjad.TemporaryDirectoryChange(directory=directory):
            lines = self._io_manager.run_command(command)
        return lines

    def _get_next_package(self, directory):
        assert directory.is_dir()
        if self._is_score_directory(directory, 'material'):
            materials_directory = directory.parent
            paths = self._list_visible_paths(materials_directory)
            index = paths.index(directory)
            paths = abjad.CyclicTuple(paths)
            path = paths[index + 1]
        elif self._is_score_directory(directory, 'materials'):
            paths = self._list_visible_paths(directory)
            path = paths[0]
        elif self._is_score_directory(directory, 'segment'):
            segments_directory = directory.parent
            paths = self._list_visible_paths(segments_directory)
            index = paths.index(directory)
            paths = abjad.CyclicTuple(paths)
            path = paths[index + 1]
        elif self._is_score_directory(directory, 'segments'):
            paths = self._list_visible_paths(directory)
            path = paths[0]
        else:
            raise ValueError(directory)
        return path

    def _get_previous_package(self, directory):
        assert directory.is_dir()
        if self._is_score_directory(directory, 'material'):
            materials_directory = directory.parent
            paths = self._list_visible_paths(materials_directory)
            index = paths.index(directory)
            paths = abjad.CyclicTuple(paths)
            path = paths[index - 1]
        elif self._is_score_directory(directory, 'materials'):
            paths = self._list_visible_paths(directory)
            path = paths[-1]
        elif self._is_score_directory(directory, 'segment'):
            segments_directory = directory.parent
            paths = self._list_visible_paths(segments_directory)
            index = paths.index(directory)
            paths = abjad.CyclicTuple(paths)
            path = paths[index - 1]
        elif self._is_score_directory(directory, 'segments'):
            paths = self._list_visible_paths(directory)
            path = paths[-1]
        else:
            raise ValueError(directory)
        return path

    def _get_previous_segment_directory(self, directory):
        assert directory.is_dir()
        segments_directory = self._to_score_directory(
            directory,
            'segments',
            )
        paths = self._list_visible_paths(segments_directory)
        for i, path in enumerate(paths):
            if path == directory:
                break
        else:
            message = 'can not find segment directory path.'
            raise Exception(message)
        current_path_index = i
        if current_path_index == 0:
            return
        previous_path_index = current_path_index - 1
        previous_path = paths[previous_path_index]
        return previous_path

    def _get_repository_root_directory(self, path):
        command = 'git rev-parse --show-toplevel'
        with abjad.TemporaryDirectoryChange(directory=path):
            lines = self._io_manager.run_command(command)
            first_line = lines[0]
            return self.Path(first_line)

    def _get_score_pdf(self, directory):
        directory = self.Path(directory)
        path = self._get_file_path_ending_with(
            directory.distribution,
            'score.pdf',
            )
        if not path:
            path = self._get_file_path_ending_with(
                directory.build,
                'score.pdf',
                )
        return path

    def _get_segment_metadata(self, directory):
        assert directory.is_dir()
        assert self._is_score_directory(directory, 'segment'), repr(directory)
        previous_directory = self._get_previous_directory(directory)
        assert self._is_score_directory(previous_directory, 'segment')
        metadata = directory._get_metadata()
        segments_directory = self._to_score_directory(directory, 'segments')
        paths = self._list_visible_paths(segments_directory)
        if directory == paths[0]:
            return metadata
        previous_metadata = previous_directory._get_metadata()
        return metadata, previous_metadata

    def _get_title_metadatum(self, score_directory, year=True):
        assert score_directory.is_dir()
        if year and score_directory._get_metadatum('year'):
            result = '{} ({})'
            result = result.format(
                self._get_title_metadatum(score_directory, year=False),
                score_directory._get_metadatum('year')
                )
            return result
        else:
            result = score_directory._get_metadatum('title')
            result = result or '(untitled score)'
            return result

    def _get_unadded_asset_paths(self, directory):
        assert directory.is_dir()
        paths = []
        root_directory = self._get_repository_root_directory(directory)
        git_status_lines = self._get_git_status_lines(directory)
        for line in git_status_lines:
            line = str(line)
            if line.startswith('?'):
                path = line.strip('?')
                path = path.strip()
                path = root_directory / path
                paths.append(path)
            elif line.startswith('M'):
                path = line.strip('M')
                path = path.strip()
                path = root_directory / path
                paths.append(path)
        paths = [_ for _ in paths]
        return paths

    def _git_add(self, directory):
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'wrapper')
        change = abjad.TemporaryDirectoryChange(directory=directory)
        interaction = self._interaction()
        with change, interaction:
            self._display(f'git add {directory} ...')
            inputs = self._get_unadded_asset_paths(directory)
            outputs = []
            nothing_message = f'{directory} ... nothing to add.'
            if not inputs:
                self._display(nothing_message)
                return False
            command = f'git add -A {directory}'
            for file_ in inputs:
                self._io_manager.run_command(command)
            messages = []
            for file_ in inputs:
                message = f'{self._trim(file_)} ... added.'
                messages.append(message)
            self._display(messages, capitalize=False)
            return True

    def _handle_input(self, result):
        prototype = (str, tuple, pathlib.Path, self.Path)
        assert isinstance(result, prototype), repr(result)
        if result == '<return>':
            return
        package_prototype = ('contents', 'material', 'segment')
        if isinstance(result, tuple):
            assert len(result) == 1, repr(result)
            result = result[0]
            message = 'unknown command: {!r}.'
            message = message.format(result)
            self._display([message, ''])
        elif isinstance(result, str) and result.startswith('!'):
            statement = result[1:]
            self._io_manager._invoke_shell(statement)
            self._display('')
        elif isinstance(result, str) and result.startswith(
            ('@', '%', '^', '*', '+')):
            directory = self._session.current_directory
            prefix = result[0]
            body = result[1:]
            line_number = None
            if '+' in body:
                index = body.find('+')
                line_number = body[index + 1:]
                if abjad.mathtools.is_integer_equivalent(line_number):
                    line_number = int(line_number)
                else:
                    line_number = None
                body = body[:index]
            path = None
            if body in ('<', '>'):
                if body == '<':
                    path = self._get_previous_package(directory)
                else:
                    path = self._get_next_package(directory)
            if path is None:
                try:
                    segment_number = int(body)
                except ValueError:
                    segment_number = None
                if segment_number:
                    path = self._segment_number_to_path(
                        directory,
                        segment_number,
                        )
            if path is None:
                path = self._match_display_string(directory, body)
            if path:
                path = self.Path(path)
                if prefix == '@':
                    if self._is_score_directory(path, ('material', 'segment')):
                        path = path / 'definition.py'
                    self._io_manager.open_file(path, line_number=line_number)
                elif prefix == '%':
                    if path.is_dir():
                        self._manage_directory(path)
                    else:
                        message = 'matches no display string: {!r}.'
                        message = message.format(result)
                        self._display([message, ''])
                elif prefix == '^':
                    interaction = self._interaction()
                    with interaction:
                        self._run_doctest(path)
                elif prefix == '*':
                    if self._is_score_directory(path, ('material', 'segment')):
                        pdf = path / 'illustration.pdf'
                        self.open_pdf(path)
                elif prefix == '+':
                    if self._is_score_directory(path, ('material', 'segment')):
                        path = path / 'definition.py'
                    directory = path.parent
                    self._io_manager.open_file(path, line_number=line_number)
                    self._manage_directory(directory)
                else:
                    raise ValueError(prefix)
            else:
                message = f'matches no display string: {result!r}.'
                self._display([message, ''])
        elif result in self._get_command_dictionary():
            command = self._get_command_dictionary()[result]
            if command.argument_name == 'current_directory':
                command(self._session.current_directory)
            else:
                command()
        elif (isinstance(result, str) and
            result.endswith('!') and
            result[:-1] in self._get_command_dictionary()):
            result = result[:-1]
            self._get_command_dictionary()[result]()
        elif self.Path(result).is_file():
            self._io_manager.open_file(result)
        elif self._is_score_directory(result, package_prototype):
            self._manage_directory(result)
        elif self._is_score_directory(result):
            self._manage_directory(result)
        else:
            message = 'unknown command: {!r}.'
            message = message.format(result)
            self._display([message, ''])

    def _has_pending_commit(self, directory):
        assert directory.is_dir()
        command = 'git status {!s}'.format(directory)
        with abjad.TemporaryDirectoryChange(directory=directory):
            lines = self._io_manager.run_command(command)
        clean_lines = []
        for line in lines:
            line = str(line)
            clean_line = line.strip()
            clean_line = clean_line.replace(str(directory), '')
            clean_lines.append(clean_line)
        for line in clean_lines:
            if 'Changes not staged for commit:' in line:
                return True
            if 'Changes to be committed:' in line:
                return True

    def _interaction(self):
        return self._io_manager._make_interaction()

    def _interpret_tex_file(self, tex_path):
        r'''Interprets TeX file.
        Calls xelatex (or pdflatex) on file TWICE.
        Some LaTeX packages (like tikz) require two passes.
        '''
        if not tex_path.is_file():
            message = f'can not find {self._trim(tex_path)} ...'
            self._display(message)
            return
        executables = self._io_manager.find_executable('xelatex')
        executables = [self.Path(_) for _ in executables]
        if not executables:
            executable_name = 'pdflatex'
            fancy_executable_name = 'LaTeX'
        else:
            executable_name = 'xelatex'
            fancy_executable_name = 'XeTeX'
        pdf_path = tex_path.parent / (str(tex_path.stem) + '.pdf')
        if pdf_path.exists():
            message = 'removing {} ...'
            message = message.format(self._trim(pdf_path))
            self._display(message)
            pdf_path.unlink()
        message = f'interpreting {self._trim(tex_path)} ...'
        self._display(message)
        command = 'date > {};'
        command += ' {} -halt-on-error'
        command += ' --jobname={} -output-directory={} {}'
        command += ' >> {!s} 2>&1'
        command = command.format(
            self._configuration.latex_log_file_path,
            executable_name,
            tex_path.stem,
            tex_path.parent,
            tex_path,
            self._configuration.latex_log_file_path,
            )
        command_called_twice = '{}; {}'.format(command, command)
        with abjad.TemporaryDirectoryChange(tex_path.parent):
            self._io_manager.spawn_subprocess(command_called_twice)
            for path in tex_path.parent.glob('*.aux'):
                path.unlink()
            for path in tex_path.parent.glob('*.log'):
                path.unlink()
            messages = []
            if pdf_path.is_file():
                error = False
                message = f'writing {self._trim(pdf_path)} ...'
            else:
                error = True
                message = 'ERROR IN LATEX LOG FILE ...'
                log_file = self._configuration.latex_log_file_path
                with log_file.open() as file_pointer:
                    lines = file_pointer.readlines()
                    messages.extend(lines)
            messages.append(message)
            return messages

    @classmethod
    def _is_build_directory_name(class_, name):
        if not isinstance(name, str):
            return False
        if not name == name.lower():
            return False
        if name[0] == '.':
            return False
        if name[0] == '_':
            return False
        return True

    @staticmethod
    def _is_classfile_name(argument):
        if not isinstance(argument, str):
            return False
        argument = pathlib.Path(argument)
        if not abjad.String(argument.stem).is_upper_camel_case():
            return False
        if not argument.suffix == '.py':
            return False
        return True

    @staticmethod
    def _is_dash_case_file_name(argument):
        if not isinstance(argument, str):
            return False
        argument = pathlib.Path(argument)
        if not argument.name == argument.name.lower():
            return False
        if not abjad.String(argument.stem).is_dash_case():
            return False
        if not argument.suffix:
            return False
        return True

    def _is_git_unknown(self, path):
        if path is None:
            return False
        if not path.exists():
            return False
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return True
        return False

    def _is_in_git_repository(self, path):
        if path is None:
            return False
        if not path.exists():
            return False
        path = self._to_score_directory(path, 'wrapper')
        path = self.Path(path)
        for path_ in path.glob('*'):
            if path_.name == '.git':
                return True
        return False

    @staticmethod
    def _is_lowercase_file_name(argument):
        if not isinstance(argument, str):
            return False
        if not argument == argument.lower():
            return False
        if not (abjad.String(pathlib.Path(argument).stem).is_snake_case() or
            abjad.String(pathlib.Path(argument).stem).is_dash_case()):
            return False
        if pathlib.Path(argument).suffix not in ('.py', '.ly', '.pdf'):
            return False
        return True

    def _is_maker_file_name(self, argument):
        if self._is_classfile_name(argument):
            return True
        if self._is_module_file_name(argument):
            return True
        return False

    @staticmethod
    def _is_module_file_name(argument):
        if not isinstance(argument, str):
            return False
        argument = pathlib.Path(argument)
        if not argument.name == argument.name.lower():
            return False
        if not abjad.String(argument.stem).is_snake_case():
            return False
        if not argument.suffix == '.py':
            return False
        return True

    @staticmethod
    def _is_package_name(argument):
        if not isinstance(argument, str):
            return False
        if not argument == argument.lower():
            return False
        if not abjad.String(argument).is_snake_case():
            return False
        return True

    @staticmethod
    def _is_public_python_file_name(argument):
        if not isinstance(argument, str):
            return False
        if pathlib.Path(argument).stem.startswith('_'):
            return False
        if not pathlib.Path(argument).suffix == '.py':
            return False
        return True

    def _is_score_directory(self, directory, prototype=()):
        if not directory.is_dir():
            return False
        if isinstance(prototype, str):
            prototype = (prototype,)
        if not prototype and self._to_scores_directory(directory):
            return True
        assert all(isinstance(_, str) for _ in prototype)
        if not self._to_scores_directory(directory):
            return False
        if 'scores' in prototype:
            if directory == self._configuration.composer_scores_directory:
                return True
            if directory == self._configuration.example_scores_directory:
                return True
        scores_directory = self._to_score_directory(directory, 'scores')
        if 'wrapper' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = directory.parts
            if len(parts) == scores_directory_parts_count + 1:
                return True
        if 'contents' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = directory.parts
            if len(parts) == scores_directory_parts_count + 2:
                if parts[-1] == parts[-2]:
                    return True
        if 'build subdirectory' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = directory.parts
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'build' and not parts[-1] == '_segments':
                    return True
        if 'material' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = directory.parts
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'materials':
                    return True
        if 'segment' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = directory.parts
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'segments':
                    return True
        if directory.name not in (
            '_segments',
            'build',
            'distribution',
            'etc',
            'tools',
            'material',
            'materials',
            'score',
            'scores',
            'segment',
            'segments',
            'stylesheets',
            'test',
            ):
            return False
        if prototype is None:
            return True
        if directory.name in prototype:
            return True
        return False

    @staticmethod
    def _is_stylesheet_name(argument):
        if not isinstance(argument, str):
            return False
        argument = pathlib.Path(argument)
        if not argument.name == argument.name.lower():
            return False
        if not abjad.String(argument.stem).is_dash_case():
            return False
        if not argument.suffix == '.ily':
            return False
        return True

    @staticmethod
    def _is_test_file_name(argument):
        if not isinstance(argument, str):
            return False
        argument = pathlib.Path(argument)
        if not argument.name.startswith('test_'):
            return False
        if not abjad.String(argument.stem).is_snake_case():
            return False
        if not argument.suffix == '.py':
            return False
        return True

    def _is_up_to_date(self, path):
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        return first_line == ''

    @staticmethod
    def _is_wrapper_directory_name(argument):
        if argument in ('.git', '.DS_Store'):
            return False
        return True

    def _list_paths(self, directory, example_scores=True):
        assert directory.is_dir()
        paths = []
        directories = self._collect_similar_directories(
            directory,
            example_scores=example_scores,
            )
        directory_ = directory
        for directory in directories:
            if not directory:
                continue
            if not directory.exists():
                continue
            name_predicate = self._to_name_predicate(directory)
            entries = sorted([_.name for _ in directory.glob('*')])
            for entry in entries:
                if not name_predicate(entry):
                    continue
                path = directory / entry
                if self._is_score_directory(directory, 'scores'):
                    path = path / entry
                try:
                    path.relative_to(directory_)
                except ValueError:
                    continue
                paths.append(path)
        return paths

    def _list_secondary_paths(self, directory):
        assert directory.is_dir()
        paths = []
        for path in directory.glob('*'):
            if path.name in sorted(self._secondary_names):
                paths.append(path)
        return paths

    def _list_visible_paths(self, directory):
        assert directory.is_dir()
        paths = self._list_paths(directory)
        strings = [self._to_menu_string(_) for _ in paths]
        entries = []
        pairs = list(zip(strings, paths))
        for string, path in pairs:
            entry = (string, None, None, path)
            entries.append(entry)
        view = self._read_view(directory)
        entries = self._filter_by_view(directory, entries, view)
        if self._is_score_directory(directory, 'scores'):
            if self._session.is_test or self._session.is_example:
                entries = [_ for _ in entries if 'Score' in _[0]]
            else:
                entries = [_ for _ in entries if 'Score' not in _[0]]
        paths = [_[-1] for _ in entries]
        if view is None and self._is_score_directory(directory, 'scores'):
            paths = self._sort_by_menu_string(paths)
        assert all(isinstance(_, self.Path) for _ in paths), repr(paths)
        return paths

    def _make_build_subdirectory(self, directory):
        assert directory.is_dir()
        getter = self._io_manager._make_getter()
        getter.append_string('subdirectory name')
        subdirectory_name = getter._run(io_manager=self._io_manager)
        if not subdirectory_name:
            return
        subdirectory_name = subdirectory_name.lower()
        subdirectory_name = subdirectory_name.replace(' ', '-')
        subdirectory_name = subdirectory_name.replace('_', '-')
        build_subdirectory = directory / subdirectory_name
        if build_subdirectory.exists():
            message = 'path already exists: {}.'
            message = message.format(self._trim(build_subdirectory))
            self._display(message)
            return
        getter = self._io_manager._make_getter()
        message = 'paper size (ex: letter or letter landscape)'
        getter.append_string(message)
        paper_size = getter._run(io_manager=self._io_manager)
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
        getter = self._io_manager._make_getter()
        message = r'price (ex: \$80 / \euro 72)'
        getter.append_string(message)
        price = getter._run(io_manager=self._io_manager)
        if price is None:
            return
        getter = self._io_manager._make_getter()
        message = 'catalog number suffix (ex: ann.)'
        getter.append_string(message)
        catalog_number_suffix = getter._run(io_manager=self._io_manager)
        file_names = (
            'back-cover.tex',
            'front-cover.tex',
            'music.ly',
            'preface.tex',
            'score.tex',
            'stylesheet.ily',
            )
        file_paths = [build_subdirectory / _ for _ in file_names]
        messages = []
        messages.append('will create ...')
        message = '   {}'.format(self._trim(build_subdirectory))
        messages.append(message)
        for file_path in file_paths:
            message = '   {}'.format(self._trim(file_path))
            messages.append(message)
        self._display(messages)
        if not self._io_manager._confirm():
            return
        if build_subdirectory.exists():
            shutil.rmtree(str(build_subdirectory))
        build_subdirectory.mkdir()
        build_subdirectory._add_metadatum('paper_size', paper_size)
        if not orientation == 'portrait':
            build_directory._add_metadatum('orientation', orientation)
        build_subdirectory._add_metadatum('price', price)
        build_subdirectory._add_metadatum(
            'catalog_number_suffix',
            catalog_number_suffix,
            )
        self.generate_back_cover(build_subdirectory)
        self.generate_front_cover(build_subdirectory)
        self.generate_music(build_subdirectory)
        self.generate_preface(build_subdirectory)
        self.generate_score(build_subdirectory)
        self.generate_build_subdirectory_stylesheet(build_subdirectory)

    def _make_command_menu_sections(self, directory, menu):
        assert directory.is_dir()
        commands = []
        outside_score_sections = (
            'back-home-quit',
            'basic',
            'display navigation',
            'git',
            'global files',
            'navigation',
            'star',
            'system',
            'tests',
            )
        for command in self._get_commands():
            forbidden_directories = command.forbidden_directories
            if (not self._is_score_directory(directory) and
                command.section in outside_score_sections):
                commands.append(command)
            elif not self._is_score_directory(directory, command.directories):
                continue
            elif (command.forbidden_directories and
                self._is_score_directory(directory, forbidden_directories)):
                continue
            else:
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
        getter = self._io_manager._make_getter()
        getter.append_string('file name')
        file_name = getter._run(io_manager=self._io_manager)
        if file_name in (None, ''):
            return
        #file_name = self._coerce_name(directory, file_name)
        file_name = directory._coerce_name(file_name)
        name_predicate = self._to_name_predicate(directory)
        if not name_predicate(file_name):
            message = 'invalid file name: {!r}.'
            message = message.format(file_name)
            self._display(message)
            self._io_manager._acknowledge()
            return
        file_path = directory / file_name
        boilerplate_directory = self._configuration.boilerplate_directory
        if self._is_score_directory(directory, 'tools'):
            if self._is_classfile_name(file_name):
                source_file = boilerplate_directory / 'Maker.py'
                shutil.copyfile(str(source_file), str(file_path))
                template = file_path.read_text()
                class_name = file_path.stem
                completed_template = template.format(class_name=class_name)
                file_path.write_text(completed_template)
            else:
                source_file = boilerplate_directory / 'make_something.py'
                shutil.copyfile(str(source_file), str(file_path))
                template = file_path.read_text()
                function_name = file_path.stem
                completed_template = template.format(
                    function_name=function_name,
                    )
                file_path.write_text(completed_template)
        else:
            contents = ''
            self._io_manager.write(file_path, contents)
        self._io_manager.edit(file_path)

    def _make_main_menu(self, directory, header):
        assert directory.is_dir()
        assert isinstance(header, str), repr(header)
        name = type(self).__name__
        name = abjad.String(name).to_space_delimited_lowercase()
        menu = self._io_manager._make_menu(
            header=header,
            name=name,
            )
        menu_entries = []
        secondary_menu_entries = self._make_secondary_menu_entries(directory)
        secondary_menu_entries = []
        for path in self._list_secondary_paths(directory):
            base_name = path.name
            menu_entry = (base_name, None, None, path)
            secondary_menu_entries.append(menu_entry)
        secondary_menu_entries.sort(key=lambda _: _[0])
        menu_entries.extend(secondary_menu_entries)
        asset_menu_entries = []
        paths = self._list_visible_paths(directory)
        strings = [self._to_menu_string(_) for _ in paths]
        if self._is_score_directory(directory, 'wrapper'):
            strings = [_.name for _ in paths]
        pairs = list(zip(strings, paths))
        for string, path in pairs:
            asset_menu_entry = (string, None, None, path)
            asset_menu_entries.append(asset_menu_entry)
        menu_entries.extend(asset_menu_entries)
        if menu_entries:
            menu.make_asset_section(menu_entries=menu_entries)
        self._make_command_menu_sections(directory, menu)
        return menu

    def _make_material_ly(self, directory):
        assert directory.is_dir()
        directory = self.Path(directory)
        assert directory.parent.name == 'materials'
        definition = directory / 'definition.py'
        if not definition.is_file():
            message = f'can not find {self._trim(definition)} ...'
            self._display(message)
            return
        source = directory / '__illustrate__.py'
        if not source.is_file():
            message = f'can not find {self._trim(source)} ...'
            self._display(message)
            return
        target = directory / 'illustration.ly'
        if target.exists():
            self._display(f'removing {self._trim(target)} ...')
        source_make = self.Path('boilerplate') / '__make_material_ly__.py'
        target_make = directory / '__make_material_ly__.py'
        with abjad.FilesystemState(remove=[target_make]):
            target_make.remove()
            shutil.copyfile(str(source_make), str(target_make))
            self._display(f'interpreting {self._trim(source)} ...')
            result = self._io_manager.interpret_file(str(target_make))
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self._display_errors(stderr_lines)
                return
            if not target.is_file():
                message = f'could not make {self._trim(target)}.'
                self._display(message)
                return
            self._display(f'writing {self._trim(target)} ...')

    def _make_material_pdf(self, directory, open_after=True):
        assert directory.is_dir()
        directory = self.Path(directory)
        assert directory.parent.name == 'materials'
        illustrate = directory / '__illustrate__.py'
        if not illustrate.is_file():
            message = f'can not find {self._trim(illustrate)} ...'
            self._display(message)
            return [], True
        definition = directory / 'definition.py'
        if not definition.is_file():
            message = f'can not find {self._trim(definition)} ...'
            self._display(message)
            return [], False
        self._display('making PDF ...')
        source = directory / 'illustration.ly'
        target = source.with_suffix('.pdf')
        boilerplate = self.Path('boilerplate')
        source_make = boilerplate / '__make_material_pdf__.py'
        target_make = directory / '__make_material_pdf__.py'
        with abjad.FilesystemState(remove=[target_make]):
            for output_file in (source, target):
                if output_file.exists():
                    message = f'removing {self._trim(output_file)} ...'
                    self._display(message)
                    output_file.remove()
            shutil.copyfile(str(source_make), str(target_make))
            message = f'interpreting {self._trim(illustrate)} ...'
            self._display(message)
            result = self._io_manager.interpret_file(target_make)
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self._display_errors(stderr_lines)
                return [], False
            if open_after:
                message = f'opening {self._trim(target)} ...'
                self._display(message)
                self._io_manager.open_file(str(target))
            return [], True

    def _make_package(self, directory):
        assert directory.is_dir()
        path = self._get_available_path(directory)
        if not path:
            return
        assert not path.exists()
        path.mkdir()
        required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )
        for required_file in required_files:
            boilerplate_directory = \
                self._configuration.boilerplate_directory
            if required_file == '__init__.py':
                source_path = boilerplate_directory / 'empty_unicode.py'
            elif required_file == '__metadata__.py':
                source_path = boilerplate_directory / '__metadata__.py'
            elif required_file == 'definition.py':
                source_path = boilerplate_directory / 'definition.py'
            else:
                raise ValueError(required_file)
            target_path = path / required_file
            shutil.copyfile(str(source_path), str(target_path))
        new_path = path
        paths = self._list_visible_paths(directory)
        if path not in paths:
            directory._clear_view()
        self._manage_directory(new_path)

    def _make_score_package(self):
        scores_directory = self._configuration.composer_scores_directory
        if self._session.is_test or self._session.is_example:
            scores_directory = self._configuration.example_scores_directory
        scores_directory = self.Path(scores_directory)
        package_name = None
        wrapper = None
        directories = self._find_empty_score_directories()
        if directories:
            directory = directories[0]
            self._display(f'found {directory}.')
            if not self._io_manager._confirm(f'populate {directory}?'):
                return
            package_name = str(directory)
            wrapper = directory
        getter = self._io_manager._make_getter()
        getter.append_string('enter title')
        title = getter._run(io_manager=self._io_manager)
        if not title:
            return
        if not wrapper:
            package_name = abjad.String(title).strip_diacritics()
            package_name = abjad.String(package_name).to_snake_case()
            wrapper = scores_directory / package_name
            if wrapper.exists():
                self._display(f'directory already exists: {wrapper}.')
                return
        self._display(f'making {wrapper} ...')
        year = datetime.date.today().year
        abjad.IOManager._make_score_package(
            score_package_path=str(wrapper),
            composer_email=self._configuration.composer_email,
            composer_full_name=self._configuration.composer_full_name,
            composer_github_username=self._configuration.composer_github_username,
            composer_last_name=self._configuration.composer_last_name,
            composer_library=self._configuration.composer_library,
            score_title=title,
            year=year,
            )
        scores_directory._clear_view()
        self._manage_directory(wrapper.contents)

    def _make_secondary_menu_entries(self, directory):
        assert directory.is_dir()
        menu_entries = []
        for path in self._list_secondary_paths(directory):
            base_name = path.name
            menu_entry = (base_name, None, None, path)
            menu_entries.append(menu_entry)
        return menu_entries

    def _make_segment_ly(self, directory):
        assert directory.is_dir()
        directory = self.Path(directory)
        assert directory.parent.name == 'segments', repr(directory)
        definition = directory / 'definition.py'
        if not definition.is_file():
            message = f'can not find {self._trim(definition)} ...'
            self._display(message)
            return
        self._update_order_dependent_segment_metadata(directory)
        boilerplate = self._configuration.boilerplate_directory
        source_make = boilerplate / '__make_segment_ly__.py'
        target_make = directory / '__make_segment_ly__.py'
        target_make.remove()
        with abjad.FilesystemState(remove=[target_make]):
            illustrate = directory / '__illustrate__.py'
            target = directory / 'illustration.ly'
            if target.exists():
                self._display(f'removing {self._trim(target)} ...')
            shutil.copyfile(str(source_make), str(target_make))
            previous_segment_path = self._get_previous_segment_directory(
                directory)
            if previous_segment_path is None:
                statement = 'previous_metadata = None'
            else:
                score_directory = self._to_score_directory(directory)
                score_name = score_directory.name
                previous_segment_name = previous_segment_path
                previous_segment_name = previous_segment_path.name
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_metadata'
                statement = statement.format(score_name, previous_segment_name)
            template = target_make.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            target_make.write_text(template)
            illustrate = directory / '__illustrate__.py'
            if illustrate.exists():
                message = f'removing {self._trim(illustrate)} ...'
                self._display(message)
                message = f'writing {self._trim(illustrate)} ...'
                self._display(message)
            message = f'interpreting {self._trim(illustrate)} ...'
            self._display(message)
            result = self._io_manager.interpret_file(target_make)
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self._display_errors(stderr_lines)
                return
            self._display(f'writing {self._trim(target)} ...')

    def _make_segment_pdf(self, directory, open_after=True):
        assert directory.is_dir()
        definition_path = directory / 'definition.py'
        if not definition_path.is_file():
            message = 'can not find {} ...'
            message = message.format(self._trim(definition_path))
            self._display(message)
            return [], False
        self._display('making PDF ...')
        self._update_order_dependent_segment_metadata(directory)
        boilerplate_directory = self._configuration.boilerplate_directory
        boilerplate_path = boilerplate_directory / '__illustrate_segment__.py'
        illustrate = directory / '__illustrate__.py'
        ly_path = directory / 'illustration.ly'
        pdf_path = directory / 'illustration.pdf'
        output_files = (ly_path, pdf_path)
        for output_file in output_files:
            if output_file.exists():
                message = 'removing {} ...'
                message = message.format(self._trim(output_file))
                self._display(message)
                output_file.unlink()
        if illustrate.exists():
            self._display(f'removing {self._trim(illustrate)} ...')
            illustrate.unlink()
        self._display(f'writing {self._trim(illustrate)} ...')
        message = 'interpreting {} ...'
        message = message.format(self._trim(illustrate))
        self._display(message)
        shutil.copyfile(str(boilerplate_path), str(illustrate))
        previous_segment_directory = self._get_previous_segment_directory(
            directory)
        if previous_segment_directory is None:
            statement = 'previous_metadata = None'
        else:
            assert previous_segment_directory.is_dir()
            score_directory = self._to_score_directory(directory)
            score_name = score_directory.name
            previous_segment_name = previous_segment_directory
            previous_segment_name = previous_segment_directory.name
            statement = 'from {}.segments.{}.__metadata__'
            statement += ' import metadata as previous_metadata'
            statement = statement.format(score_name, previous_segment_name)
        template = illustrate.read_text()
        completed_template = template.format(
            previous_segment_metadata_import_statement=statement
            )
        illustrate.write_text(completed_template)
        result = self._io_manager.interpret_file(illustrate)
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self._display_errors(stderr_lines)
            return [], False
        log_file_path = abjad.abjad_configuration.lilypond_log_file_path
        log_file_path = self.Path(log_file_path)
        with log_file_path.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                message = 'ERROR IN LILYPOND LOG FILE ...'
                self._display(message)
                break
        if pdf_path.is_file() and open_after:
            message = f'opening {self._trim(pdf_path)} ...'
            self._display(message)
            self._io_manager.open_file(pdf_path)
        return [], True

    def _manage_directory(self, directory):
        directory = self.Path(directory)
        if not directory.exists():
            message = f'directory does not exist: {self._trim(directory)}.'
            self._display(message)
            return
        self._session._pending_redraw = True
        if not self._session.current_directory == directory:
            self._session._previous_directory = \
                self._session.current_directory
            self._session._current_directory = directory
        menu_header = self._to_menu_header(directory)
        menu = self._make_main_menu(directory, menu_header)
        while True:
            if not self._session.current_directory == directory:
                self._session._previous_directory = \
                    self._session.current_directory
                self._session._current_directory = directory
            os.chdir(str(directory))
            if self._session._pending_menu_rebuild:
                menu = self._make_main_menu(directory, menu_header)
                self._session._pending_menu_rebuild = False
            result = menu._run(io_manager=self._io_manager)
            if isinstance(result, tuple):
                assert len(result) == 1, repr(result)
                unknown_string = result[0]
                result_ = self._match_alias(directory, unknown_string)
                is_executable, path = result_
                if is_executable:
                    with self._interaction():
                        self._io_manager.spawn_subprocess(str(path))
                elif path and not path.exists():
                    if path.suffix:
                        self._io_manager.edit(path, allow_missing=True)
                elif path:
                    if path.is_file():
                        self._io_manager.open_file(path)
                        parent_directory = path.parent
                        names = ('material', 'segment')
                        if self._is_score_directory(parent_directory, names):
                            self._manage_directory(parent_directory)
                    elif path.is_dir():
                        self._manage_directory(path)
                    else:
                        message = 'file does not exist: {}.'
                        message = message.format(self._trim(path))
                        self._display([message, ''])
                if path:
                    result = None
            prototype = (str, tuple, type(None), self.Path)
            assert isinstance(result, prototype), repr(result)
            if self._session.is_quitting:
                return
            if result is None:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                continue
            if (isinstance(result, pathlib.Path) and
                not isinstance(result, self.Path)):
                result = self.Path(result)
            self._handle_input(result)
            if self._session.is_quitting:
                return

    def _match_alias(self, directory, string):
        assert directory.is_dir()
        is_executable = False
        aliases = self._configuration.aliases
        if not aliases:
            return is_executable, None
        value = self._configuration.aliases.get(string)
        if not value:
            return is_executable, None
        if value.startswith('!'):
            is_executable = True
            value = value[1:]
        path = self.Path(value)
        if path.exists():
            return is_executable, path
        if (self._is_score_directory(directory) and
            not self._is_score_directory(directory, 'scores')):
            score_directory = self._to_score_directory(directory, 'contents')
            path = score_directory / value
            return is_executable, path
        return is_executable, None

    def _match_display_string(self, directory, argument):
        assert directory.is_dir()
        strings, paths = self._collect_all_display_strings(directory)
        for string, path in zip(strings, paths):
            if string == argument:
                return path
        for string, path in zip(strings, paths):
            if string.startswith(argument):
                return path
        for string, path in zip(strings, paths):
            if argument in string:
                return path
        initial_strings = []
        initial_paths = []
        for string, path in zip(strings, paths):
            string = self.Path(string).stem
            words = abjad.String(string).delimit_words()
            initial_letters = [_[0] for _ in words]
            if not initial_letters:
                continue
            initial_string = ''.join(initial_letters)
            initial_strings.append(initial_string)
            initial_paths.append(path)
        pairs = zip(initial_strings, initial_paths)
        for initial_string, initial_path in pairs:
            if initial_string == argument:
                return initial_path

    @staticmethod
    def _match_display_string_view_pattern(pattern, entry):
        display_string, _, _, path = entry
        token = ':ds:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(display_string))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            result = False
        return result

    def _match_metadata_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        count = pattern.count('md:')
        for _ in range(count + 1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = path._get_metadatum(metadatum_name)
                    metadatum = repr(metadatum)
                    pattern = pattern.replace(part, metadatum)
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    @staticmethod
    def _match_path_view_pattern(pattern, entry):
        display_string, _, _, path = entry
        token = ':path:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(path))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_visible_path(self, secondary_paths, visible_paths, input_):
        assert isinstance(input_, (str, int)), repr(input_)
        paths = secondary_paths + visible_paths
        if isinstance(input_, int):
            path_number = input_
            path_index = path_number - 1
            path = paths[path_index]
            if path in secondary_paths:
                message = 'can not modify secondary asset {}.'
                message = message.format(self._trim(path))
                self._display(message)
                return
            return path
        elif isinstance(input_, str):
            name = input_
            name = name.lower()
            for path in visible_paths:
                base_name = path.name
                base_name = base_name.lower()
                if base_name.startswith(name):
                    return path
                base_name = base_name.replace('_', ' ')
                if base_name.startswith(name):
                    return path
                if not path.is_dir():
                    continue
                title = path._get_metadatum('title')
                if title:
                    title = title.lower()
                    if title.startswith(name):
                        return path
                name_ = path._get_metadatum('name')
                if name_:
                    if name_ == input_:
                        return path
            message = 'does not match visible path: {!r}.'
            message = message.format(name)
            self._display(message)
            return
        else:
            raise ValueError(repr(input_))

    def _open_every_file(self, paths):
        for path in paths:
            message = f'opening {self._trim(path)} ...'
            self._display(message)
        if paths:
            self._io_manager.open_file(paths)

    def _parse_paper_size(self, directory):
        assert directory.is_dir()
        score_directory = self._to_score_directory(directory)
        string = score_directory._get_metadatum('paper_size')
        string = string or '8.5 x 11 in'
        parts = string.split()
        assert len(parts) == 4
        width, _, height, units = parts
        width = eval(width)
        height = eval(height)
        return width, height, units

    def _read_view(self, directory):
        assert directory.is_dir()
        view_name = directory._get_metadatum('view_name')
        if not view_name:
            return
        view_inventory = self._read_view_inventory(directory)
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self, directory):
        assert directory.is_dir()
        views_py_path = directory / '__views__.py'
        result = self._io_manager.execute_file(
            path=views_py_path,
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            messages = []
            message = '{} __views.py__ is corrupt:'
            message = message.format(self._trim(directory))
            messages.append(message)
            messages.append('')
            message = '    {}'.format(views_py_path)
            messages.append(message)
            self._display(messages)
            return
        if not result:
            return
        assert len(result) == 1
        view_inventory = result[0]
        if view_inventory is None:
            view_inventory = abjad.TypedOrderedDict()
        items = list(view_inventory.items())
        view_inventory = abjad.TypedOrderedDict(items)
        return view_inventory

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
        self._display(f'running doctest on {self._trim(path)} ...')
        command = f'ajv doctest -x {path}'
        self._io_manager.spawn_subprocess(command)

    def _run_lilypond(self, ly_path):
        assert ly_path.exists()
        if not abjad.IOManager.find_executable('lilypond'):
            message = 'cannot find LilyPond executable.'
            raise ValueError(message)
        directory = ly_path.parent
        pdf_path = ly_path.with_suffix('.pdf')
        backup_pdf_path = ly_path.with_suffix('._backup.pdf')
        if backup_pdf_path.exists():
            backup_pdf_path.unlink()
        directory_change = abjad.TemporaryDirectoryChange(directory)
        filesystem_state = abjad.FilesystemState(remove=[backup_pdf_path])
        with directory_change, filesystem_state:
            messages = []
            if pdf_path.exists():
                message = f'removing {self._trim(pdf_path)} ...'
                messages.append(message)
                shutil.move(str(pdf_path), str(backup_pdf_path))
                assert not pdf_path.exists()
            else:
                backup_pdf_path = None
            messages.append(f'interpreting {self._trim(ly_path)} ...')
            abjad.IOManager.run_lilypond(str(ly_path))
            if not pdf_path.is_file():
                message = 'can not produce {} ...'
                message = message.format(self._trim(pdf_path))
                messages.append(message)
                if backup_pdf_path:
                    message = f'restoring {self._trim(backup_pdf_path)} ...'
                    messages.append(message)
                    shutil.move(str(backup_pdf_path), str(pdf_path))
            messages.append(f'writing {self._trim(pdf_path)} ...')
            return messages

    def _run_pytest(self, path):
        assert path.exists()
        self._display(f'running pytest on {self._trim(path)} ...')
        command = f'py.test -xrf {path}'
        self._io_manager.spawn_subprocess(command)

    def _segment_number_to_path(self, directory, segment_number):
        assert directory.is_dir()
        segments_directory = self._to_score_directory(directory, 'segments')
        for path in segments_directory.glob('*'):
            if not path.is_dir():
                continue
            if not path.name.startswith('segment_'):
                continue
            body = path.name[8:]
            try:
                body = int(body)
            except ValueError:
                continue
            if body == segment_number:
                return path

    def _select_path_to_copy(self, directory, more=False):
        assert directory.is_dir()
        example_scores = self._session.is_test or self._session.is_example
        if more:
            directories = self._collect_similar_directories(
                directory,
                example_scores=example_scores,
                )
        else:
            directories = [directory]
        paths = []
        for directory_ in directories:
            for path in directory_.glob('*'):
                if path.name.endswith('.pyc'):
                    continue
                if path.name.startswith('.'):
                    continue
                if path.name == '__pycache__':
                    continue
                paths.append(path)
        trimmed_paths = [str(self._trim(_)) for _ in paths]
        menu_header = self._to_menu_header(directory)
        menu_header = menu_header + ' - select:'
        selector = self._io_manager._make_selector(
            items=trimmed_paths,
            menu_header=menu_header,
            )
        trimmed_source = selector._run(io_manager=self._io_manager)
        if (trimmed_source != ('more',) and
            trimmed_source != ('less',) and
            trimmed_source not in trimmed_paths):
            return
        elif trimmed_source == ('more',):
            trimmed_source = self._select_path_to_copy(
                directory,
                more=True,
                )
        elif trimmed_source == ('less',):
            trimmed_source = self._select_path_to_copy(directory)
        if not trimmed_source:
            return
        return trimmed_source

    def _select_view(self, directory, is_ranged=False):
        assert directory.is_dir()
        view_inventory = self._read_view_inventory(directory)
        if view_inventory is None:
            message = 'no views found.'
            self._display(message)
            return
        view_names = list(view_inventory.keys())
        view_names.append('none')
        if is_ranged:
            target_name = 'view(s)'
        else:
            target_name = 'view'
        target_name = '{} to apply'.format(target_name)
        menu_header = self._to_menu_header(directory)
        selector = self._io_manager._make_selector(
            is_ranged=is_ranged,
            items=view_names,
            menu_header=menu_header,
            target_name=target_name,
            )
        result = selector._run(io_manager=self._io_manager)
        if result is None:
            return
        return result

    def _select_visible_path(self, directory, infinitive_phrase=None):
        assert directory.is_dir()
        secondary_paths = self._list_secondary_paths(directory)
        visible_paths = self._list_visible_paths(directory)
        if not visible_paths:
            message = 'no visible paths'
            if infinitive_phrase is not None:
                message = message + ' ' + infinitive_phrase
            message = message + '.'
            self._display(message)
            return
        asset_identifier = self._to_asset_identifier(directory)
        message = 'enter {}'.format(asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        getter = self._io_manager._make_getter()
        getter.append_string_or_integer(message)
        result = getter._run(io_manager=self._io_manager)
        if not result:
            return
        path = self._match_visible_path(secondary_paths, visible_paths, result)
        return path

    def _select_visible_paths(self, directory, infinitive_phrase=None):
        assert directory.is_dir()
        secondary_paths = self._list_secondary_paths(directory)
        visible_paths = self._list_visible_paths(directory)
        if not visible_paths:
            message = 'no visible paths'
            if infinitive_phrase is not None:
                message = message + ' ' + infinitive_phrase
            message = message + '.'
            self._display(message)
            return
        paths = secondary_paths + visible_paths
        asset_identifier = self._to_asset_identifier(directory)
        message = 'enter {}(s)'
        if infinitive_phrase is not None:
            message += ' ' + infinitive_phrase
        message = message.format(asset_identifier)
        getter = self._io_manager._make_getter()
        getter.append_anything(message)
        result = getter._run(io_manager=self._io_manager)
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
        paths = []
        for input_ in result:
            path = self._match_visible_path(
                secondary_paths,
                visible_paths,
                input_,
                )
            if path:
                paths.append(path)
        return paths

    def _sort_by_menu_string(self, paths):
        strings = [self._to_menu_string(_) for _ in paths]
        pairs = list(zip(strings, paths))

        def sort_function(pair):
            string = pair[0]
            string = abjad.String(string).strip_diacritics()
            string = string.replace("'", '')
            return string
        pairs.sort(key=lambda _: sort_function(_))
        paths = [_[-1] for _ in pairs]
        return paths

    def _start(self, input_=None):
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        self._session._pending_redraw = True
        directory = self._configuration.composer_scores_directory
        if self._session.is_test or self._session.is_example:
            directory = self._configuration.example_scores_directory
        while True:
            self._manage_directory(directory)
            if self._session.is_quitting:
                break
        self._io_manager._clean_up()
        self._io_manager.clear_terminal()

    def _to_asset_identifier(self, directory):
        assert directory.is_dir()
        file_prototype = (
            'build',
            'build subdirectory',
            'distribution',
            'etc',
            'tools',
            'material',
            'segment',
            'stylesheets',
            'test',
            )
        package_prototype = (
            'scores',
            'materials',
            'segments',
            )
        if self._is_score_directory(directory, package_prototype):
            return 'package'
        elif self._is_score_directory(directory, file_prototype):
            return 'file'
        else:
            raise ValueError(directory)

    def _to_menu_header(self, directory):
        assert directory.is_dir()
        header_parts = []
        if self._is_score_directory(directory, 'scores'):
            return 'Abjad IDE - scores directory'
        score_directory = self._to_score_directory(directory)
        if not self._is_score_directory(directory):
            header = 'Abjad IDE - {}'
            header = header.format(directory)
            return header
        score_part = self._get_title_metadatum(score_directory)
        header_parts.append(score_part)
        if self._is_score_directory(directory, 'wrapper'):
            header_parts.append('wrapper directory')
        trimmed_path = self._trim(directory)
        path_parts = self.Path(trimmed_path).parts
        path_parts = path_parts[1:]
        if not path_parts:
            directory_part, package_part = None, None
        elif self._is_score_directory(directory, ('contents', 'wrapper')):
            directory_part, package_part = None, None
        elif len(path_parts) == 1:
            directory_part, package_part = path_parts[0], None
        elif len(path_parts) == 2:
            directory_part, package_part = path_parts
        else:
            message = f'can not classify {directory!r}.'
            raise ValueError(message, path_parts)
        if directory_part:
            directory_part = directory_part + ' directory'
            header_parts.append(directory_part)
        if package_part:
            if package_part == '_segments':
                package_part = 'segments'
            else:
                package_part = package_part.replace('_', ' ')
            package_part = directory._get_metadatum('name', package_part)
            header_parts.append(package_part)
        header = ' - '.join(header_parts)
        return header

    def _to_menu_string(self, path):
        assert isinstance(path, self.Path), repr(path)
        if self._is_score_directory(path, 'contents'):
            annotation = None
            metadata = path._get_metadata()
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                annotation = path.name
            return annotation
        if self._is_score_directory(path, 'segment'):
            name = path._get_metadatum('name')
            if name is not None:
                return name
        prototype = ('tools', 'wrapper', 'test')
        if ('_' in path.name and
            self._is_score_directory(path) and
            not self._is_score_directory(path, prototype)):
            return abjad.String(path.name).to_space_delimited_lowercase()
        return path.name

    def _to_module_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = name.lower()
        name = self.Path(name).stem
        name = abjad.String(name).to_snake_case()
        name = name + '.py'
        assert self._is_module_file_name(name), repr(name)
        return name

    def _to_name_predicate(self, directory):
        assert directory.is_dir()
        file_prototype = ('distribution', 'etc')
        package_prototype = ('materials', 'segments', 'scores')
        if not self._is_score_directory(directory):
            return self._is_public_python_file_name
        elif self._is_score_directory(directory, 'build'):
            return self._is_build_directory_name
        elif self._is_score_directory(directory, 'build subdirectory'):
            return self._is_dash_case_file_name
        elif self._is_score_directory(directory, '_segments'):
            return self._is_dash_case_file_name
        elif self._is_score_directory(directory, file_prototype):
            return self._is_dash_case_file_name
        elif self._is_score_directory(directory, package_prototype):
            return self._is_package_name
        elif self._is_score_directory(directory, 'scores'):
            return self._is_package_name
        elif self._is_score_directory(directory, 'wrapper'):
            return self._is_wrapper_directory_name
        elif self._is_score_directory(directory, ('score', 'contents')):
            return self._is_package_name
        elif self._is_score_directory(directory, 'tools'):
            return self._is_maker_file_name
        elif self._is_score_directory(directory, ('material', 'segment')):
            return self._is_lowercase_file_name
        elif self._is_score_directory(directory, 'stylesheets'):
            return self._is_stylesheet_name
        elif self._is_score_directory(directory, 'test'):
            return self._is_module_file_name
        else:
            raise ValueError(directory)

    def _to_paper_dimensions(self, paper_size, orientation='portrait'):
        prototype = ('landscape', 'portrait', None)
        assert orientation in prototype, repr(orientation)
        paper_dimensions = self._paper_size_to_paper_dimensions[paper_size]
        paper_dimensions = paper_dimensions.replace(' x ', ' ')
        width, height, unit = paper_dimensions.split()
        if orientation == 'landscape':
            height_ = width
            width_ = height
            height = height_
            width = width_
        return width, height, unit

    def _to_score_directory(self, path, name=None):
        if path.is_dir() and not self._is_score_directory(path):
            return path
        scores_directory = self._to_scores_directory(path)
        if name == 'scores':
            return scores_directory
        parts = path.relative_to(scores_directory).parts
        if not parts:
            return
        score_name = parts[0]
        score_directory = scores_directory / score_name / score_name
        if name in ('contents', 'score'):
            pass
        elif name == 'wrapper':
            score_directory = score_directory.parent
        elif name is not None:
            score_directory = score_directory / name
        return score_directory

    def _to_scores_directory(self, path):
        string = str(path)
        for scores_directory in (
            self._configuration.composer_scores_directory,
            self._configuration.example_scores_directory):
            if string.startswith(str(scores_directory)):
                return scores_directory

    def _trim(self, path):
        assert isinstance(path, self.Path), repr(path)
        scores_directory = self._to_scores_directory(path)
        if scores_directory is None:
            return str(path)
        if self._is_score_directory(path, ('wrapper', 'contents')):
            return str(path)
        count = len(scores_directory.parts) + 1
        parts = path.parts
        parts = parts[count:]
        return str(pathlib.Path(*parts))

    @staticmethod
    def _trim_ly(ly_path):
        assert ly_path.is_file()
        lines = []
        with ly_path.open() as file_pointer:
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

    def _unadd_added_assets(self, path):
        paths = []
        paths.extend(self._get_added_asset_paths(path))
        paths.extend(self._get_modified_asset_paths(path))
        commands = []
        for path in paths:
            command = 'git reset -- {!s}'.format(path)
            commands.append(command)
        command = ' && '.join(commands)
        with abjad.TemporaryDirectoryChange(directory=path):
            self._io_manager.spawn_subprocess(command)

    def _update_order_dependent_segment_metadata(self, directory):
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'segments')
        paths = self._list_visible_paths(directory)
        if not paths:
            return
        segment_count = len(paths)
        # update segment numbers and segment count
        for segment_index, path in enumerate(paths):
            segment_number = segment_index + 1
            path._add_metadatum('segment_number', segment_number)
            path._add_metadatum('segment_count', segment_count)
        # update first bar numbers and measure counts
        path = paths[0]
        first_bar_number = 1
        path._add_metadatum('first_bar_number', first_bar_number)
        measure_count = path._get_metadatum('measure_count')
        if not measure_count:
            return
        next_bar_number = first_bar_number + measure_count
        for path in paths[1:]:
            first_bar_number = next_bar_number
            path._add_metadatum('first_bar_number', next_bar_number)
            measure_count = path._get_metadatum('measure_count')
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count

    def _write_metadata_py(self, directory, metadata):
        assert directory.is_dir()
        metadata_py_path = directory / '__metadata__.py'
        lines = []
        lines.append('import abjad')
        lines.append('')
        lines.append('')
        contents = '\n'.join(lines)
        metadata = abjad.TypedOrderedDict(metadata)
        items = list(metadata.items())
        items.sort()
        metadata = abjad.TypedOrderedDict(items)
        metadata_lines = format(metadata, 'storage')
        metadata_lines = 'metadata = {}'.format(metadata_lines)
        contents = contents + '\n' + metadata_lines + '\n'
        metadata_py_path.write_text(contents)

    ### PUBLIC METHODS ###

    @Command(
        'bld',
        argument_name='current_directory',
        description='score pdf - build',
        directories=('build subdirectory',),
        section='build',
        )
    def build_score(self, directory):
        r'''Builds score from the ground up.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('building score ...')
            self.collect_segment_lys(directory.contents)
            self.generate_music(directory)
            self.interpret_music(directory)
            tex_file_path = directory.build / 'front-cover.tex'
            pdf_path = directory.build / 'front-cover.pdf'
            if tex_file_path:
                self.interpret_front_cover(directory)
            elif pdf_path:
                message = f'using existing {self._trim(pdf_path)} ...'
                self._display(message)
            else:
                self._display('can make front cover ...')
                return
            tex_file_path = directory.build / 'preface.tex'
            pdf_path = directory.build / 'preface.pdf'
            if tex_file_path:
                self.interpret_preface(directory)
            elif pdf_path:
                message = f'using existing {self._trim(pdf_path)} ...'
                self._display(message)
            else:
                self._display('can make front cover ...')
                return
            tex_file_path = directory.build / 'back-cover.tex'
            pdf_path = directory.build / 'back-cover.pdf'
            if tex_file_path:
                self.interpret_back_cover(directory)
            elif pdf_path:
                message = f'using existing {self._trim(pdf_path)} ...'
                self._display(message)
            else:
                self._display('can make front covert ...')
                return
            self.generate_score(directory)
            messages = self.interpret_score(directory)
            target = directory / 'score.pdf'
            message = f'opening {self._trim(target)} ...'
            self._display(message)
            self._io_manager.open_file(target)

    @Command(
        'dfk',
        argument_name='current_directory',
        description='definition file - check',
        directories=('material', 'segment',),
        section='definition_file',
        )
    def check_definition_file(self, directory):
        r'''Checks definition file.

        Returns exit code 1 on failure.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('checking definition file ...')
            definition = directory / 'definition.py'
            if not definition.is_file():
                message = f'can not find {self._trim(definition)} ...'
                message = message.format(self._trim(definition))
                self._display(message)
                return
            with abjad.Timer() as timer:
                result = self._io_manager.interpret_file(definition)
            stdout_lines, stderr_lines, exit_code = result
            self._display(stdout_lines)
            if exit_code:
                messages = [str(definition) + ' FAILED:']
                messages.extend(stderr_lines)
                self._display(messages)
            else:
                message = f'{self._trim(definition)} ... OK'
                self._display(message, capitalize=False)
            self._display(timer.total_time_message)
            return exit_code

    @Command(
        'dfk*',
        argument_name='current_directory',
        description='every definition file - check',
        directories=('materials', 'segments'),
        section='star',
        )
    def check_every_definition_file(self, directory):
        r'''Checks definition file in every package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        paths = self._list_visible_paths(directory)
        for path in paths:
            self.check_definition_file(path)

    @Command(
        'lyc',
        argument_name='current_directory',
        description='segment lys - collect',
        directories=('build', 'build subdirectory',),
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
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('collecting segment lys ...')
            directory = self._to_score_directory(directory)
            pairs = self._collect_segment_lys(directory)
            if not pairs:
                message = '... no segment lys found.'
                self._display(message)
                return
            build_directory = self._to_score_directory(directory, 'build')
            _segments_directory = build_directory / '_segments'
            if not _segments_directory.is_dir():
                _segments_directory.mkdir()
            messages = []
            for source_ly_path, target_ly_path in pairs:
                if target_ly_path.exists():
                    message = f'removing {self._trim(target_ly_path)} ...'
                    self._display(message)
                message = f'writing {self._trim(target_ly_path)} ...'
                self._display(message)
                text = self._trim_ly(source_ly_path)
                target_ly_path.write_text(text)

    @Command(
        'cp',
        argument_name='current_directory',
        forbidden_directories=('contents',),
        section='basic',
        )
    def copy(self, directory):
        r'''Copies into `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            trimmed_source = self._select_path_to_copy(directory)
            if not trimmed_source:
                return
            trimmed_source = self.Path(trimmed_source)
            scores_directory = self._configuration.composer_scores_directory
            if self._session.is_test or self._session.is_example:
                scores_directory = self._configuration.example_scores_directory
            score_name = trimmed_source.parts[0]
            source_path = scores_directory / score_name / trimmed_source
            asset_name = source_path.name
            target_path = directory / asset_name
            if source_path == target_path:
                message = '{} already exists.'
                message = message.format(self._trim(target_path))
                self._display(message, capitalize=False)
                getter = self._io_manager._make_getter()
                getter.append_string('enter new name')
                name = getter._run(io_manager=self._io_manager)
                if not name:
                    return
                directory_name = target_path.name
                target_path = directory_name / name
            if source_path == target_path:
                return
            if source_path.is_file():
                shutil.copyfile(str(source_path), str(target_path))
            elif source_path.is_dir():
                shutil.copytree(str(source_path), str(target_path))
            else:
                raise ValueError(source_path)
            self._display(f'writing {self._trim(target_path)} ...')

    @Command('?', section='system')
    def display_action_command_help(self):
        r'''Displays action commands.

        Returns none.
        '''
        pass

    @Command(';', section='display navigation')
    def display_navigation_command_help(self):
        r'''Displays navigation commands.

        Returns none.
        '''
        pass

    @Command(
        'als',
        description='aliases - edit',
        section='global files',
        )
    def edit_aliases_file(self):
        r'''Edits aliases file.

        Returns none.
        '''
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        path = self._configuration.aliases_file_path
        self._io_manager.edit(path)
        self._configuration._read_aliases_file()

    @Command(
        'bce',
        argument_name='current_directory',
        description='back cover - edit',
        directories=('build subdirectory'),
        section='build-edit',
        )
    def edit_back_cover_source(self, directory):
        r'''Edits ``back-cover.tex`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'back-cover.tex'
        self._io_manager.open_file(file_path)

    @Command(
        'df',
        argument_name='current_directory',
        description='definition file - edit',
        directories=('material', 'segment',),
        section='definition_file',
        )
    def edit_definition_file(self, directory):
        r'''Edits definition file.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        definition_path = directory / 'definition.py'
        self._io_manager.edit(definition_path)

    @Command(
        'ee*',
        argument_name='current_directory',
        description='every string - edit',
        section='star',
        )
    def edit_every(self, directory):
        r'''Opens Vim and goes to every occurrence of search string.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            getter = self._io_manager._make_getter()
            getter.append_string('enter search string')
            search_string = getter._run(io_manager=self._io_manager)
            if not search_string:
                return
            command = r'vim -c "grep {!s} --type=python"'
            command = command.format(search_string)
            if directory == self._to_scores_directory(directory):
                pass
            else:
                directory = self._to_score_directory(directory, 'wrapper')
            directory = abjad.TemporaryDirectoryChange(directory)
            with directory:
                self._io_manager.spawn_subprocess(command)

    @Command(
        'df*',
        argument_name='current_directory',
        description='every definition file - edit',
        directories=('materials', 'segments'),
        section='star',
        )
    def edit_every_definition_file(self, directory):
        r'''Edits definition file in every subdirectory of `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            directories = self._list_visible_paths(directory)
            paths = [_ / 'definition.py' for _ in directories]
            self._open_every_file(paths)

    @Command(
        'ff*',
        argument_name='current_directory',
        description='every file - edit',
        section='star',
        )
    def edit_every_file(self, directory):
        r'''Edits files in every subdirectory of `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            getter = self._io_manager._make_getter()
            getter.append_string('enter filename')
            name = getter._run(io_manager=self._io_manager)
            if not name:
                return
            command = 'find {!s} -name {}'
            command = command.format(directory, name)
            paths = self._io_manager.run_command(command)
            self._io_manager.open_file(paths)

    @Command(
        'fce',
        argument_name='current_directory',
        description='front cover - edit',
        directories=('build subdirectory'),
        section='build-edit',
        )
    def edit_front_cover_source(self, directory):
        r'''Edits ``front-cover.tex`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'front-cover.tex'
        self._io_manager.open_file(file_path)

    @Command(
        'ill',
        argument_name='current_directory',
        description='illustrate file - edit',
        directories=('material',),
        section='illustrate_file',
        )
    def edit_illustrate_file(self, directory):
        r'''Edits illustrate file.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        illustrate_py_path = directory / '__illustrate__.py'
        self._io_manager.edit(illustrate_py_path)

    @Command(
        'lxg',
        description='latex log - edit',
        section='global files',
        )
    def edit_latex_log(self):
        r'''Edits LaTeX log.

        Returns none.
        '''
        self._session._attempted_to_open_file = True
        with self._interaction():
            target = self._configuration.latex_log_file_path
            if not target.is_file():
                self._display(f'missing {target} ...')
            else:
                self._display(f'opening {target} ...')
                self._io_manager.open_file(target)

    @Command(
        'lpg',
        description='lilypond log - edit',
        section='global files',
        )
    def edit_lilypond_log(self):
        r'''Edits LilyPond log.

        Returns none.
        '''
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        self._io_manager.open_last_log()

    @Command(
        'ly',
        argument_name='current_directory',
        description='ly - edit',
        directories=('material', 'segment',),
        section='ly',
        )
    def edit_ly(self, directory):
        r'''Edits ``illustration.ly`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'illustration.ly'
        self._io_manager.open_file(file_path)

    @Command(
        'me',
        argument_name='current_directory',
        description='music - edit',
        directories=('build subdirectory'),
        section='build-edit',
        )
    def edit_music_source(self, directory):
        r'''Edits ``music.ly`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'music.ly'
        self._io_manager.open_file(file_path)

    @Command(
        'pe',
        argument_name='current_directory',
        description='preface - edit',
        directories=('build subdirectory'),
        section='build-edit',
        )
    def edit_preface_source(self, directory):
        r'''Edits ``preface.tex`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'preface.tex'
        self._io_manager.open_file(file_path)

    @Command(
        'se',
        argument_name='current_directory',
        description='score - edit',
        directories=('build subdirectory'),
        section='build-edit',
        )
    def edit_score_source(self, directory):
        r'''Edits ``score.tex`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'score.tex'
        self._io_manager.open_file(file_path)

    @Command(
        'ste',
        argument_name='current_directory',
        description='stylesheet - edit',
        directories=('build subdirectory'),
        section='build-edit',
        )
    def edit_stylesheet(self, directory):
        r'''Edits ``stylesheet.ily`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'stylesheet.ily'
        self._io_manager.open_file(file_path)

    @Command(
        'bcg',
        argument_name='current_directory',
        description='back cover - generate',
        directories=('build subdirectory'),
        section='build-generate',
        )
    def generate_back_cover(self, directory):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        contents = directory.contents
        with self._interaction():
            self._display('generating back cover ...')
            replacements = {}
            catalog_number = contents._get_metadatum('catalog_number')
            name = 'catalog_number_suffix'
            catalog_number_suffix = contents._get_metadatum(name)
            if catalog_number_suffix:
                catalog_number += f' / {catalog_number_suffix}'
            replacements['catalog_number'] = catalog_number
            composer_website = self._configuration.composer_website or ''
            if self._session.is_test or self._session.is_example:
                composer_website = 'www.composer-website.com'
            replacements['composer_website'] = composer_website
            price = contents._get_metadatum('price', r'\null')
            replacements['price'] = price
            paper_size = contents._get_metadatum('paper_size', 'letter')
            orientation = contents._get_metadatum('orientation')
            paper_size = self._to_paper_dimensions(paper_size, orientation)
            width, height, unit = paper_size
            paper_size = f'{{{width}{unit}, {height}{unit}}}'
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                'back-cover.tex',
                directory,
                replacements=replacements,
                )
            self._display(messages)

    @Command(
        'stg',
        argument_name='current_directory',
        description='stylesheet - generate',
        directories=('build subdirectory',),
        section='build-generate',
        )
    def generate_build_subdirectory_stylesheet(self, directory):
        r'''Generates build subdirectory ``stylsheet.ily``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('generating subdirectory stylesheet ...')
            replacements = {}
            paper_size = directory._get_metadatum('paper_size')
            orientation = directory._get_metadatum('orientation')
            replacements['paper_size'] = paper_size
            if orientation:
                orientation_ = " '{}".format(orientation)
            else:
                orientation_ = ''
            replacements['orientation'] = orientation_
            messages = self._copy_boilerplate(
                'build-subdirectory-stylesheet.ily',
                directory,
                target_file_name='stylesheet.ily',
                replacements=replacements,
                )
            self._display(messages)

    @Command(
        'fcg',
        argument_name='current_directory',
        description='front cover - generate',
        directories=('build subdirectory',),
        section='build-generate',
        )
    def generate_front_cover(self, directory):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            contents = directory.contents
            self._display('generating front cover ...')
            file_name = 'front-cover.tex'
            replacements = {}
            score_title = contents._get_title_metadatum(year=False)
            score_title = score_title.upper()
            replacements['score_title'] = score_title
            forces_tagline = contents._get_metadatum('forces_tagline', '')
            replacements['forces_tagline'] = forces_tagline
            year = contents._get_metadatum('year', '')
            replacements['year'] = str(year)
            composer = self._configuration.composer_uppercase_name
            if self._session.is_test or self._session.is_example:
                composer = 'COMPOSER'
            replacements['composer'] = str(composer)
            paper_size = contents._get_metadatum('paper_size', 'letter')
            orientation = contents._get_metadatum('orientation')
            paper_size = self._to_paper_dimensions(paper_size, orientation)
            width, height, unit = paper_size
            paper_size = f'{{{width}{unit}, {height}{unit}}}'
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                file_name,
                directory,
                replacements=replacements,
                )
            self._display(messages)

    @Command(
        'mg',
        argument_name='current_directory',
        description='music - generate',
        directories=('build subdirectory',),
        section='build-generate',
        )
    def generate_music(self, directory):
        r'''Generates ``music.ly``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        contents = directory.contents
        with self._interaction():
            self._display('generating music ...')
            target = directory / 'music.ly'
            if target.exists():
                message = f'removing {self._trim(target)} ...'
                self._display(message)
                target.unlink()
            messages = []
            ly_paths = self._list_visible_paths(contents.segments)
            if ly_paths:
                view_name = contents.segments._get_metadatum('view_name')
                views = self._read_view_inventory(contents.segments)
                if not views or view_name not in views:
                    view_name = None
                if view_name:
                    message = f'examining segments in {view_name!r} order ...'
                    messages.append(message)
                else:
                    message = 'examining segments in alphabetical order ...'
                    messages.append(message)
            else:
                messages.append('no segments found ...')
            for ly_path in ly_paths:
                messages.append(f'examining {self._trim(ly_path)} ...')
            self._display(messages)
            segment_names = []
            for ly_path in ly_paths:
                segment_name = ly_path.stem
                segment_names.append(segment_name)
            lilypond_names = [_.replace('_', '-') for _ in segment_names]
            source_path = self.Path('boilerplate') / 'music.ly'
            target = directory / 'music.ly'
            message = f'writing {self._trim(target)} ...'
            self._display(message)
            shutil.copyfile(str(source_path), str(target))
            lines = []
            segment_include_statements = ''
            for i, lilypond_name in enumerate(lilypond_names):
                file_name = lilypond_name + '.ly'
                line = r'\include "../_segments/{}"'
                if 0 < i:
                    line = self._tab + line
                line = line.format(file_name)
                lines.append(line)
            if lines:
                new = '\n'.join(lines)
                segment_include_statements = new
            stylesheet_include_statement = ''
            if self._is_score_directory(directory, 'build'):
                line = r'\include "../stylesheets/stylesheet.ily"'
            elif self._is_score_directory(
                directory,
                'build subdirectory',
                ):
                line = r'\include "stylesheet.ily"'
            stylesheet_include_statement = line
            language_token = abjad.LilyPondLanguageToken()
            lilypond_language_directive = format(language_token)
            version_token = abjad.LilyPondVersionToken()
            lilypond_version_directive = format(version_token)
            annotated_title = contents._get_title_metadatum(year=True)
            if annotated_title:
                score_title = annotated_title
            else:
                score_title = contents._get_title_metadatum(year=False)
            forces_tagline = contents._get_metadatum('forces_tagline', '')
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
        argument_name='current_directory',
        description='preface - generate',
        directories=('build subdirectory',),
        section='build-generate',
        )
    def generate_preface(self, directory):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        subdirectory = directory
        assert subdirectory.is_build_subdirectory, repr(subdirectory)
        with self._interaction():
            self._display('generating preface ...')
            replacements = {}
            paper_size = subdirectory._get_metadatum('paper_size', 'letter')
            orientation = subdirectory._get_metadatum('orientation')
            paper_size = self._to_paper_dimensions(paper_size, orientation)
            width, height, unit = paper_size
            paper_size = f'{{{width}{unit}, {height}{unit}}}'
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                'preface.tex',
                subdirectory,
                replacements=replacements,
                )
            self._display(messages)

    @Command(
        'sg',
        argument_name='current_directory',
        description='score - generate',
        directories=('build subdirectory',),
        section='build-generate',
        )
    def generate_score(self, directory):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        subdirectory = directory
        assert subdirectory.is_build_subdirectory, repr(subdirectory)
        with self._interaction():
            self._display('generating score ...')
            replacements = {}
            paper_size = subdirectory._get_metadatum('paper_size', 'letter')
            orientation = subdirectory._get_metadatum('orientation')
            paper_size = self._to_paper_dimensions(paper_size, orientation)
            width, height, unit = paper_size
            paper_size = f'{{{width}{unit}, {height}{unit}}}'
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                'score.tex',
                directory,
                replacements=replacements,
                )
            self._display(messages)

    @Command(
        'add*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_add_every_package(self, directory):
        r'''Adds every asset to repository.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self._session._attempted_method = 'git_add_every_package'
        if self._session.is_test:
            return
        directories = self._list_visible_paths(directory)
        for directory in directories:
            self._git_add(directory)

    @Command(
        'ci',
        argument_name='current_directory',
        description='git - commit',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_commit(self, directory, commit_message=None):
        r'''Commits working copy of current score package to repository.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self._io_manager._session._attempted_method = 'git_commit'
        self._display(f'git commit {directory} ...')
        if self._io_manager._session.is_test:
            return
        if not self._git_add(directory):
            return
        directory = self._to_score_directory(directory, 'wrapper')
        change = abjad.TemporaryDirectoryChange(directory=directory)
        interaction = self._interaction()
        with change, interaction:
            pending_commit = self._has_pending_commit(directory)
            if pending_commit:
                self._display(pending_commit)
            else:
                message = f'{directory} ... nothing to commit.'
                messages = [message]
                self._display(messages)
                return
            if commit_message is None:
                self._display('')
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run(io_manager=self._io_manager)
                if not commit_message:
                    return
            message = str(directory)
            scores_directory = self._configuration.example_scores_directory
            message = message.replace(str(scores_directory), '')
            scores_directory = self._configuration.composer_scores_directory
            message = message.replace(str(scores_directory), '')
            message = message + ' ...'
            command = f'git commit -m "{commit_message}" {directory}; git push'
            lines = self._io_manager.run_command(command)
            self._display(lines, capitalize=False)

    @Command(
        'ci*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_commit_every_package(self, directory):
        r'''Commits every asset to repository.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        assert self._is_score_directory(directory, 'scores'), repr(directory)
        self._session._attempted_method = 'git_commit_every_package'
        getter = self._io_manager._make_getter()
        getter.append_string('commit message')
        commit_message = getter._run(io_manager=self._io_manager)
        if not commit_message:
            return
        directories = self._list_visible_paths(directory)
        for directory in directories:
            self.git_commit(directory, commit_message=commit_message)

    @Command(
        'diff',
        argument_name='current_directory',
        description='git - diff',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_diff(self, directory):
        r'''Displays Git diff of files in current directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with abjad.TemporaryDirectoryChange(directory=directory):
            command = 'git diff {!s}'.format(directory)
            self._io_manager._session._attempted_method = 'git_diff'
            with abjad.TemporaryDirectoryChange(directory=directory):
                self._io_manager.spawn_subprocess(command)

    @Command(
        'pull',
        argument_name='current_directory',
        description='git - pull',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_pull(self, directory):
        r'''Updates working copy of current score package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self._session._attempted_method = 'git_pull'
        directory = self._to_score_directory(directory, 'wrapper')
        change = abjad.TemporaryDirectoryChange(directory=directory)
        interaction = self._interaction()
        with change, interaction:
            self._display(f'git pull {directory} ...')
            if self._io_manager._session.is_test:
                return
            root_directory = self._get_repository_root_directory(directory)
            command = f'git pull {root_directory}'
            lines = self._io_manager.run_command(command)
            if lines and 'Already up-to-date' in lines[-1]:
                lines = lines[-1:]
            self._display(lines)

    @Command(
        'pull*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_pull_every_package(self, directory):
        r'''Updates every asset from repository.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self._session._attempted_method = 'git_pull_every_package'
        directories = self._list_visible_paths(directory)
        for directory in directories:
            message = self._to_menu_string(directory)
            if message.endswith(')'):
                index = message.find('(')
                message = message[:index]
                message = message.strip()
            message = message + ':'
            self.git_pull(directory)

    @Command(
        'st',
        argument_name='current_directory',
        description='git - status',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_status(self, directory):
        r'''Displays Git status of current score package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self._io_manager._session._attempted_method = 'git_status'
        directory = self.Path(directory)
        directory = directory.wrapper
        change = abjad.TemporaryDirectoryChange(directory=directory)
        interaction = self._interaction()
        with change, interaction:
            message = f'git status {directory} ...'
            self._display(message)
            command = f'git status {directory}'
            self._io_manager.spawn_subprocess(command)

    @Command(
        'st*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_status_every_package(self, directory):
        r'''Displays Git status of every package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self._session._attempted_method = 'git_status_every_package'
        directories = self._list_visible_paths(directory)
        for directory in directories:
            self.git_status(directory)

    @Command(
        '-',
        description='back',
        section='back-home-quit',
        )
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        directory = self._session.previous_directory
        if directory:
            self._manage_directory(directory)

    @Command(
        'bb',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_build_directory(self, directory):
        r'''Goes to build directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'build')
        self._manage_directory(directory)

    @Command(
        'cc',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_contents_directory(self, directory):
        r'''Goes to contents directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory)
        self._manage_directory(directory)

    @Command(
        'dd',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_distribution_directory(self, directory):
        r'''Goes to distribution directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'distribution')
        self._manage_directory(directory)

    @Command(
        'ee',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_etc_directory(self, directory):
        r'''Goes to etc directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'etc')
        self._manage_directory(directory)

    @Command(
        'mm',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_materials_directory(self, directory):
        r'''Goes to materials directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'materials')
        self._manage_directory(directory)

    @Command(
        '>',
        argument_name='current_directory',
        directories=('material', 'materials', 'segment', 'segments'),
        section='sibling navigation',
        )
    def go_to_next_package(self, directory):
        r'''Goes to next package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._get_next_package(directory)
        self._manage_directory(directory)

    @Command(
        '<',
        argument_name='current_directory',
        directories=('material', 'materials', 'segment', 'segments'),
        section='sibling navigation',
        )
    def go_to_previous_package(self, directory):
        r'''Goes to previous package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._get_previous_package(directory)
        self._manage_directory(directory)

    @Command(
        'ss',
        section='scores',
        )
    def go_to_scores_directory(self):
        r'''Goes to scores directory.

        Returns none.
        '''
        directory = self._configuration.composer_scores_directory
        if self._session.is_test or self._session.is_example:
            directory = self._configuration.example_scores_directory
        self._manage_directory(directory)

    @Command(
        'gg',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_segments_directory(self, directory):
        r'''Goes to segments directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'segments')
        self._manage_directory(directory)

    @Command(
        'yy',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_stylesheets_directory(self, directory):
        r'''Goes to stylesheets directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'stylesheets')
        self._manage_directory(directory)

    @Command(
        'tt',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_test_directory(self, directory):
        r'''Goes to test directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'test')
        self._manage_directory(directory)

    @Command(
        'oo',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_tools_directory(self, directory):
        r'''Goes to tools directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'tools')
        self._manage_directory(directory)

    @Command(
        'ww',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_wrapper_directory(self, directory):
        r'''Goes to wrapper directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'wrapper')
        self._manage_directory(directory)

    @Command(
        'bci',
        argument_name='current_directory',
        description='back cover - interpret',
        directories=('build subdirectory',),
        section='build-interpret',
        )
    def interpret_back_cover(self, directory):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting back cover ...')
            source = directory / 'back-cover.tex'
            target = source.with_suffix('.pdf')
            messages = self._interpret_tex_file(source)
            self._display(messages)
            if target.is_file():
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        'lyi*',
        argument_name='current_directory',
        description='every ly - interpret',
        directories=('materials', 'segments'),
        section='star',
        )
    def interpret_every_ly(self, directory):
        r'''Interprets LilyPond file in every directory.

        Makes PDF in every directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting every ly ...')
            directories = self._list_visible_paths(directory)
            sources = []
            for directory in directories:
                source = directory / 'illustration.ly'
                if source.is_file():
                    sources.append(source)
            if not sources:
                message = 'no LilyPond files found.'
                message._io_manager._display(message)
                return
            with abjad.Timer() as timer:
                for source in sources:
                    self.interpret_ly(source.parent, open_after=False)
                self._display(timer.total_time_message)

    @Command(
        'fci',
        argument_name='current_directory',
        description='front cover - interpret',
        directories=('build subdirectory',),
        section='build-interpret',
        )
    def interpret_front_cover(self, directory):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting front cover ...')
            source = directory / 'front-cover.tex'
            target = source.with_suffix('.pdf')
            messages = self._interpret_tex_file(source)
            self._display(messages)
            if target.is_file():
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        'lyi',
        argument_name='current_directory',
        description='ly - interpret',
        directories=('material', 'segment',),
        section='ly',
        )
    def interpret_ly(self, directory, open_after=True):
        r'''Interprets illustration ly in `directory`.

        Makes illustration PDF.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting ly ...')
            source = directory / 'illustration.ly'
            target = source.with_suffix('.pdf')
            if source.is_file():
                messages = self._run_lilypond(source)
                self._display(messages)
            else:
                message = f'the file {self._trim(source)} does not exist.'
                self._display(message)
            if target.is_file() and open_after:
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        'mi',
        argument_name='current_directory',
        description='music - interpret',
        directories=('build subdirectory',),
        section='build-interpret',
        )
    def interpret_music(self, directory):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting music ...')
            source = directory / 'music.ly'
            target = source.with_suffix('.pdf')
            if not source.is_file():
                message = f'can not find {self._trim(source)} ...'
                self._display(message)
                return
            messages = self._run_lilypond(source)
            self._display(messages)
            if target.is_file():
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        'pi',
        argument_name='current_directory',
        description='preface - interpret',
        directories=('build subdirectory',),
        section='build-interpret',
        )
    def interpret_preface(self, directory):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting preface ...')
            source = directory / 'preface.tex'
            target = source.with_suffix('.pdf')
            messages = self._interpret_tex_file(source)
            self._display(messages)
            if target.is_file():
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        'si',
        argument_name='current_directory',
        description='score - interpret',
        directories=('build subdirectory',),
        section='build-interpret',
        )
    def interpret_score(self, directory):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('interpreting score ...')
            source = directory / 'score.tex'
            target = source.with_suffix('.pdf')
            messages = self._interpret_tex_file(source)
            self._display(messages)
            if target.is_file():
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        '!',
        section='system',
        )
    def invoke_shell(self):
        r'''Invokes shell.

        Returns none.
        '''
        with self._interaction():
            statement = self._io_manager._handle_input(
                '$',
                include_chevron=False,
                include_newline=False,
                )
            statement = statement.strip()
            self._io_manager._invoke_shell(statement)

    @Command(
        'pdfm*',
        argument_name='current_directory',
        description='every pdf - make',
        directories=('materials', 'segments'),
        section='star',
        )
    def make_every_pdf(self, directory):
        r'''Makes PDF in every directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        assert self._is_score_directory(directory, ('materials', 'segments'))
        directories = self._list_visible_paths(directory)
        for directory in directories:
            self.make_pdf(directory, open_after=False)

    @Command(
        'illm',
        argument_name='current_directory',
        description='illustrate file - make',
        directories=('material',),
        section='illustrate_file',
        )
    def make_illustrate_file(self, directory):
        r'''Makes illustrate file.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        assert directory.parent.name == 'materials'
        with self._interaction():
            contents = directory.contents
            score_package_name = contents.name
            material_package_name = directory.name
            source = self.Path('boilerplate') / '__illustrate_material__.py'
            target = directory / '__illustrate__.py'
            if target.is_file():
                message = f'preserving {self._trim(target)} ...'
                self._display(message)
                return
            message = f'writing {self._trim(target)} ...'
            self._display(message)
            shutil.copyfile(str(source), str(target))
            template = target.read_text()
            completed_template = template.format(
                score_package_name=score_package_name,
                material_package_name=material_package_name,
                )
            target.write_text(completed_template)

    @Command(
        'lym',
        argument_name='current_directory',
        description='ly - make',
        directories=('material', 'segment',),
        section='ly',
        )
    def make_ly(self, directory):
        r'''Makes illustration ly.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            self._display('making ly ...')
            if self._is_score_directory(directory, 'material'):
                self._make_material_ly(directory)
            elif self._is_score_directory(directory, 'segment'):
                self._make_segment_ly(directory)
            else:
                raise ValueError(directory)

    @Command(
        'pdfm',
        argument_name='current_directory',
        description='pdf - make',
        directories=('material', 'segment',),
        section='pdf',
        )
    def make_pdf(self, directory, open_after=True):
        r'''Makes illustration PDF.

        Returns exit code 1 on failure.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            if self._is_score_directory(directory, 'material'):
                messages, success = self._make_material_pdf(
                    directory,
                    open_after=open_after,
                    )
            elif self._is_score_directory(directory, 'segment'):
                messages, success = self._make_segment_pdf(
                    directory,
                    open_after=open_after
                    )
            else:
                raise ValueError(directory)
            assert messages == [], repr(messages)
        exit_code = not success
        return exit_code

    @Command(
        'new',
        argument_name='current_directory',
        forbidden_directories=('contents',),
        section='basic',
        )
    def new(self, directory):
        r'''Makes new asset.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            package_prototype = ('materials', 'segments')
            if self._is_score_directory(directory, 'scores'):
                self._make_score_package()
            elif self._is_score_directory(directory, package_prototype):
                self._make_package(directory)
            elif self._is_score_directory(directory, 'build'):
                self._make_build_subdirectory(directory)
            else:
                self._make_file(directory)

    @Command(
        'bc',
        argument_name='current_directory',
        description='back cover - open',
        directories=('build subdirectory'),
        section='build-open',
        )
    def open_back_cover_pdf(self, directory):
        r'''Opens ``back-cover.pdf`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'back-cover.pdf'
        self._io_manager.open_file(file_path)

    @Command(
        'pdf*',
        argument_name='current_directory',
        description='every pdf - open',
        directories=('build subdirectory', 'materials', 'scores', 'segments'),
        section='star',
        )
    def open_every_pdf(self, directory):
        r'''Opens PDF in every package.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            pdfs = []
            if self._is_score_directory(directory, 'scores'):
                directories = self._list_visible_paths(directory)
                for directory in directories:
                    pdf = self._get_score_pdf(directory)
                    if pdf is None:
                        continue
                    pdfs.append(pdf)
            else:
                paths = self._list_visible_paths(directory)
                for path in paths:
                    if str(path).endswith('.pdf'):
                        pdfs.append(path)
                    elif path.is_dir():
                        for pdf_ in path.glob('*.pdf'):
                            pdfs.append(pdf_)
            self._open_every_file(pdfs)

    @Command(
        'fc',
        argument_name='current_directory',
        description='front cover - open',
        directories=('build subdirectory'),
        section='build-open',
        )
    def open_front_cover_pdf(self, directory):
        r'''Opens ``front-cover.pdf`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'front-cover.pdf'
        self._io_manager.open_file(file_path)

    @Command(
        'm',
        argument_name='current_directory',
        description='music - open',
        directories=('build subdirectory'),
        section='build-open',
        )
    def open_music_pdf(self, directory):
        r'''Opens ``music.pdf`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'music.pdf'
        self._io_manager.open_file(file_path)

    @Command(
        'pdf',
        argument_name='current_directory',
        description='pdf - open',
        directories=('material', 'segment',),
        section='pdf',
        )
    def open_pdf(self, directory):
        r'''Opens illustration PDF.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            target = directory / 'illustration.pdf'
            if not target.is_file():
                self._display(f'missing {self._trim(target)} ...')
            else:
                self._display(f'opening {self._trim(target)} ...')
                self._io_manager.open_file(target)

    @Command(
        'p',
        argument_name='current_directory',
        description='preface - open',
        directories=('build subdirectory'),
        section='build-open',
        )
    def open_preface_pdf(self, directory):
        r'''Opens ``preface.pdf`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'preface.pdf'
        self._io_manager.open_file(file_path)

    @Command(
        'so',
        argument_name='current_directory',
        description='score pdf - open',
        directories=('contents',),
        section='pdf',
        )
    def open_score_pdf(self, directory):
        r'''Opens ``score.pdf``.

        Returns score PDF path.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_name = 'score.pdf'
        directory = directory / 'distribution'
        with self._interaction():
            path = self._get_score_pdf(directory)
            if path:
                message = f'opening {self._trim(path)} ...'
                self._display(message)
                self._io_manager.open_file(path)
            else:
                message = 'missing score PDF'
                message += ' in distribution and build directories ...'
                self._display(message)

    @Command(
        's',
        argument_name='current_directory',
        description='score - open',
        directories=('build subdirectory'),
        section='build-open',
        )
    def open_score_pdf_in_build_directory(self, directory):
        r'''Opens ``score.pdf`` in `directory`.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        file_path = directory / 'score.pdf'
        self._io_manager.open_file(file_path)

    @property
    def Path(self):
        r'''Gets IDE path class.

        Returns IDE path class.
        '''
        import ide
        return ide.Path

    @Command(
        'spp',
        argument_name='current_directory',
        description='score pdf - publish',
        directories=('build subdirectory',),
        section='build',
        )
    def publish_score_pdf(self, directory):
        r'''Publishes score PDF in distribution directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        assert directory.parent.name == 'build', repr(directory)
        with self._interaction():
            self._display('publishing score PDF ...')
            source = directory / 'score.pdf'
            if not source.exists():
                self._display(f'missing {self._trim(source)} ...')
                return
            package_name = directory.contents.name
            package_name = package_name.replace('_', '-')
            if package_name.endswith('-score'):
                target_name = f'{package_name}.pdf'
            else:
                target_name = f'{package_name}-score.pdf'
            target = directory.distribution / target_name
            self._display(f' FROM: {self._trim(source)}')
            self._display(f'   TO: {self._trim(target)}')
            shutil.copyfile(str(source), str(target))

    @Command(
        'q',
        description='quit',
        section='back-home-quit',
        )
    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True

    @Command(
        'rm',
        argument_name='current_directory',
        forbidden_directories=('contents',),
        section='basic',
        )
    def remove(self, directory):
        r'''Removes file or directory.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            paths = self._select_visible_paths(directory, 'to remove')
            if not paths:
                return
            count = len(paths)
            messages = []
            if count == 1:
                message = f'will remove {self._trim(paths[0])}'
                messages.append(message)
            else:
                messages.append('will remove ...')
                for path in paths:
                    message = f'    {self._trim(path)}'
                    messages.append(message)
            self._display(messages)
            if count == 1:
                confirmation_string = 'remove'
            else:
                confirmation_string = f'remove {count}'
            message = f"type {confirmation_string!r} to proceed"
            getter = self._io_manager._make_getter()
            getter.append_string(message)
            result = getter._run(io_manager=self._io_manager)
            if result is None:
                return
            if not result == confirmation_string:
                return
            for path in paths:
                if self._is_score_directory(path, 'contents'):
                    path = self._to_score_directory(path, 'wrapper')
                if self._is_in_git_repository(path):
                    if self._is_git_unknown(path):
                        command = f'rm -rf {path}'
                    else:
                        command = f'git rm --force -r {path}'
                else:
                    command = f'rm -rf {path}'
                with abjad.TemporaryDirectoryChange(directory=path.parent):
                    message = f'removing {self._trim(path)} ...'
                    self._display(message)
                    self._io_manager.run_command(command)
                executables = self._io_manager.find_executable('trash')
                executables = [self.Path(_) for _ in executables]
                if executables and executables[0].is_file():
                    executable = executables[0]
                    cleanup_command = str(executable) + f' {path}'
                else:
                    cleanup_command = f'rm -rf {path}'
                cleanup_command = cleanup_command.format(path)
                self._io_manager.run_command(cleanup_command)

    @Command(
        'ren',
        argument_name='current_directory',
        forbidden_directories=('contents',),
        section='basic',
        )
    def rename(self, directory):
        r'''Renames asset.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            source_path = self._select_visible_path(directory, 'to rename')
            if self._is_score_directory(source_path, 'contents'):
                source_path = source_path.parent
            if not source_path:
                return
            message = 'Will rename]> {}'
            message = message.format(self._trim(source_path))
            self._display(message)
            getter = self._io_manager._make_getter()
            getter.append_string('new name or return to cancel')
            original_target_name = getter._run(io_manager=self._io_manager)
            if not original_target_name:
                return
            #target_name = self._coerce_name(directory, original_target_name)
            target_name = directory._coerce_name(original_target_name)
            source_name = source_path.name
            target_path = source_path.parent / target_name
            if target_path.exists():
                message = 'path already exists: {!r}.'
                message = message.format(self._trim(target_path))
                self._display(message)
                return
            messages = []
            messages.append('will rename ...')
            message = ' FROM: {}'.format(self._trim(source_path))
            messages.append(message)
            message = '   TO: {}'.format(self._trim(target_path))
            messages.append(message)
            self._display(messages)
            if not self._io_manager._confirm():
                return
            shutil.move(str(source_path), str(target_path))
            if target_path.is_dir():
                for path in sorted(target_path.glob('*.py')):
                    self._replace_in_file(
                        path,
                        source_name,
                        target_name,
                        )
            if self._is_score_directory(target_path, 'wrapper'):
                false_contents_directory = target_path / source_name
                assert false_contents_directory.exists()
                true_contents_directory = target_path / target_name
                shutil.move(
                    str(false_contents_directory),
                    str(true_contents_directory),
                    )
                true_contents_directory._add_metadatum(
                    'title',
                    original_target_name,
                    )
                for path in sorted(true_contents_directory.glob('*.py')):
                    self._replace_in_file(
                        path,
                        source_name,
                        target_name,
                        )

    @Command(
        'rp',
        argument_name='current_directory',
        section='system',
        )
    def replace(self, directory):
        r'''Replaces expression.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        change = abjad.TemporaryDirectoryChange(directory)
        with self._interaction(), change:
            getter = self._io_manager._make_getter()
            getter.append_string('enter search string')
            search_string = getter._run(io_manager=self._io_manager)
            if not search_string:
                return
            getter = self._io_manager._make_getter()
            getter.append_string('enter replace string')
            replace_string = getter._run(io_manager=self._io_manager)
            if not replace_string:
                return
            complete_words = False
            result = self._io_manager._confirm('complete words only?')
            if result:
                complete_words = True
            command = 'ajv replace {!r} {!r} -Y'
            command = command.format(search_string, replace_string)
            if complete_words:
                command += ' -W'
            if directory == self._to_scores_directory(directory):
                pass
            else:
                directory = self._to_score_directory(directory, 'wrapper')
            directory = abjad.TemporaryDirectoryChange(directory)
            with directory:
                lines = self._io_manager.run_command(command)
            lines = [_.strip() for _ in lines if not _ == '']
            self._display(lines, capitalize=False)

    @Command(
        'dt',
        argument_name='current_directory',
        description='doctest - run',
        forbidden_directories=('scores',),
        section='tests',
        )
    def run_doctest(self, directory):
        r'''Runs doctest on entire score.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'contents')
        interaction = self._interaction()
        change = abjad.TemporaryDirectoryChange(directory=directory)
        with interaction, change:
            self._run_doctest(directory)

    @Command(
        'pt',
        argument_name='current_directory',
        description='pytest - run',
        forbidden_directories=('scores',),
        section='tests',
        )
    def run_pytest(self, directory):
        r'''Runs pytest on entire score.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        directory = self._to_score_directory(directory, 'contents')
        interaction = self._interaction()
        change = abjad.TemporaryDirectoryChange(directory=directory)
        with interaction, change:
            self._run_pytest(directory)

    @Command(
        'tests',
        argument_name='current_directory',
        description='tests - run',
        forbidden_directories=('scores',),
        section='tests',
        )
    def run_tests(self, directory):
        r'''Runs doctest and pytest on entire score.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        self.run_doctest(directory)
        self.run_pytest(directory)

    @Command(
        'sr',
        argument_name='current_directory',
        section='system',
        )
    def search(self, directory):
        r'''Searches for expression

        Delegates to ack if ack is found.

        Delegates to grep is ack is not found.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        with self._interaction():
            executables = self._io_manager.find_executable('ack')
            if not executables:
                executables = self._io_manager.find_executable('grep')
            executables = [self.Path(_) for _ in executables]
            if not executables:
                messages = []
                messages.append('can not find ack.')
                messages.append('can not find grep.')
                self._display(messages)
                return
            assert 1 <= len(executables)
            executable = None
            for path in executables:
                if path.is_file():
                    executable = path
            if executable is None:
                messages = []
                messages.append('can not find ack.')
                messages.append('can not find grep.')
                self._display(messages)
                return
            getter = self._io_manager._make_getter()
            getter.append_string('enter search string')
            search_string = getter._run(io_manager=self._io_manager)
            if not search_string:
                return
            if executable.name == 'ack':
                command = r'{!s} --ignore-dir=_docs {} --type=python'
                command = command.format(executable, search_string)
            elif executable.name == 'grep':
                command = r'{!s} -r {!r} *'
                command = command.format(executable, search_string)
            if directory == self._configuration.composer_scores_directory:
                pass
            elif directory == self._configuration.example_scores_directory:
                pass
            else:
                directory = self._to_score_directory(directory, 'wrapper')
            directory = abjad.TemporaryDirectoryChange(directory)
            with directory:
                lines = self._io_manager.run_command(command)
            self._display(lines, capitalize=False)

    @Command(
        'illt',
        argument_name='current_directory',
        description='illustrate file - trash',
        directories=('material',),
        section='illustrate_file',
        )
    def trash_illustrate(self, directory):
        r'''Trashes illustration file.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        illustration_file_path = directory / '__illustrate__.py'
        with self._interaction():
            if illustration_file_path.is_file():
                self._io_manager._trash_file(illustration_file_path)

    @Command(
        'lyt',
        argument_name='current_directory',
        description='ly - trash',
        directories=('material', 'segment',),
        section='ly',
        )
    def trash_ly(self, directory):
        r'''Trashes illustration LilyPond file.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        ly_file_path = directory / 'illustration.ly'
        with self._interaction():
            if ly_file_path.is_file():
                self._io_manager._trash_file(ly_file_path)

    @Command(
        'trash',
        argument_name='current_directory',
        description='ly & pdf - trash',
        directories=('material', 'segment',),
        section='ly & pdf',
        )
    def trash_ly_and_pdf(self, directory):
        r'''Trashes illustration LilyPond file and illustration PDF.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        ly_file_path = directory / 'illustration.ly'
        pdf_file_path = directory / 'illustration.pdf'
        with self._interaction():
            if ly_file_path.is_file():
                self._io_manager._trash_file(ly_file_path)
            if pdf_file_path.is_file():
                self._io_manager._trash_file(pdf_file_path)

    @Command(
        'pdft',
        argument_name='current_directory',
        description='pdf - trash',
        directories=('material', 'segment',),
        section='pdf',
        )
    def trash_pdf(self, directory):
        r'''Trashes illustration PDF.

        Returns none.
        '''
        assert isinstance(directory, self.Path)
        assert directory.is_dir()
        pdf_file_path = directory / 'illustration.pdf'
        with self._interaction():
            if pdf_file_path.is_file():
                self._io_manager._trash_file(pdf_file_path)
