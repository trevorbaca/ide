import abjad
import baca
import importlib
import os
import pathlib
from .Configuration import Configuration


class Path(abjad.Path):
    r'''Path.
    '''

    ### CLASS VARIABLES ###

    address_characters = {
        '@': 'file',
        '%': 'directory',
        '^': 'source file',
        '*': 'PDF',
        '+': 'test file',
        }

    configuration = Configuration()

    test_score_names = (
        'blue_score',
        'green_score',
        'red_score',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *arguments, scores=None):
        if not arguments:
            raise Exception('must provide at least one argument.')
        argument = arguments[0]
        _arguments = arguments[1:]
        if isinstance(argument, pathlib.Path) or os.sep in argument:
            self = pathlib.Path.__new__(class_, argument)
        else:
            arguments = []
            if argument in Path.test_score_names:
                arguments.append(Path.configuration.test_scores_directory)
                arguments.extend(2 * [argument])
            elif argument == 'boilerplate':
                arguments.append(
                    abjad.abjad_configuration.boilerplate_directory)
            elif argument == 'test_scores':
                arguments.append(Path.configuration.test_scores_directory)
            elif scores is not None:
                arguments.append(scores)
                arguments.extend(2 * [argument])
            else:
                arguments.append(
                    abjad.abjad_configuration.composer_scores_directory)
                arguments.extend(2 * [argument])
            arguments.extend(_arguments)
            self = pathlib.Path.__new__(class_, *arguments)
        if scores is not None:
            scores = type(self)(scores)
        self._scores = scores
        return self

    ### PRIVATE METHODS ###

    def _deactivate_bar_line_adjustment(self):
        counts, skippeds, messages = [], [], []
        # activate all barline adjustment tags:
        count, skipped, messages_ = self.activate(abjad.tags.EOL_FERMATA)
        counts.append(count)
        skippeds.append(skipped)
        messages.extend(messages_)
        if count == skipped == 0:
            return counts, skippeds, messages
        # then deactivate non-EOL tags:
        bol_measure_numbers = self.get_metadatum('bol_measure_numbers')
        if not bol_measure_numbers:
            return counts, skippeds, messages
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        last_measure_number = self.get_metadatum('last_measure_number')
        if last_measure_number is not None:
            eol_measure_numbers.append(last_measure_number)
        eol_measure_numbers = [f'MEASURE_{_}' for _ in eol_measure_numbers]
        tag = abjad.tags.EOL_FERMATA
        tags_ = eol_measure_numbers
        count, skipped, messages_ = self.deactivate(
            lambda tags: tag in tags and not bool(set(tags) & set(tags_)),
            name=f'{tag} (found at end-of-line)',
            )
        counts.append(count)
        skippeds.append(skipped)
        messages.extend(messages_)
        return counts, skippeds, messages

    def _deactivate_shifted_clef_at_bol(self):
        counts, skippeds, messages = [], [], []
        # activate all shifted clefs
        count, skipped, messages_ = self.activate(abjad.tags.SHIFTED_CLEF)
        counts.append(count)
        skippeds.append(skipped)
        messages.extend(messages_)
        if count == skipped == 0:
            return counts, skippeds, messages
        # then deactivate shifted clefs at BOL:
        bol_measure_numbers = self.get_metadatum('bol_measure_numbers')
        if not bol_measure_numbers:
            return counts, messages
        bol_measure_numbers = [f'MEASURE_{_}' for _ in bol_measure_numbers]
        def match(tags):
            if abjad.tags.SHIFTED_CLEF not in tags:
                return False
            if any(_ in tags for _ in bol_measure_numbers):
                return True
            return False
        count, skipped, messages_ = self.deactivate(
            match,
            name=abjad.tags.SHIFTED_CLEF,
            )
        counts.append(count)
        skippeds.append(skipped)
        messages.extend(messages_)
        return counts, skippeds, messages

    def _find_doctest_files(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob('**/*.py')):
                if '__pycache__' in str(path):
                    continue
                if not path.is_file():
                    continue
                if path.name.startswith('test'):
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.segments.list_paths():
                files.append(path('definition.py'))
                strings.append(path.get_identifier())
            for path in self.materials.list_paths():
                files.append(path('definition.py'))
                strings.append(path.get_identifier())
            for path in self.tools.list_paths():
                files.append(path)
                strings.append(path.name)
        return files, strings

    def _find_editable_files(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob('**/*')):
                if '__pycache__' in str(path):
                    continue
                if not path.is_file():
                    continue
                if path.suffix in self.configuration.noneditor_suffixes:
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.segments.list_paths():
                files.append(path('definition.py'))
                strings.append(path.get_identifier())
            for path in self.materials.list_paths():
                files.append(path('definition.py'))
                strings.append(path.get_identifier())
            for path in self.tools.list_paths():
                files.append(path)
                strings.append(path.name)
            for path in self.stylesheets.list_paths():
                files.append(path)
                strings.append(path.name)
            for path in self.etc.list_paths():
                files.append(path)
                strings.append(path.name)
        return files, strings

    def _find_pdfs(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob('**/*.pdf')):
                if '__pycache__' in str(path):
                    continue
                if not path.is_file():
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.segments.list_paths():
                files.append(path('illustration.pdf'))
                strings.append(path.get_identifier())
            for path in self.materials.list_paths():
                files.append(path('illustration.pdf'))
                strings.append(path.get_identifier())
            for path in self.etc.list_paths():
                if path.suffix == '.pdf':
                    files.append(path)
                    strings.append(path.name)
        return files, strings

    def _find_pytest_files(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob('**/test*.py')):
                if '__pycache__' in str(path):
                    continue
                if not path.is_file():
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.test.list_paths():
                files.append(path)
                strings.append(path.name)
        return files, strings

    def _get_added_asset_paths(self):
        paths = []
        git_status_lines = self._get_git_status_lines()
        for line in git_status_lines:
            line = str(line)
            if line.startswith('A'):
                path = line.strip('A')
                path = path.strip()
                root = self.wrapper
                path = root / path
                paths.append(path)
        return paths

    def _get_git_status_lines(self):
        with abjad.TemporaryDirectoryChange(directory=self.wrapper):
            command = f'git status --porcelain {self}'
            return abjad.IOManager.run_command(command)

    def _get_part_manifest(self):
        assert self.is_score_package_path()
        score_package_name = self.contents.name
        try:
            module = importlib.import_module(score_package_name)
        except:
            return -1, f'can not import {score_package_name!r}.'
        if not hasattr(module, 'tools'):
            return -1, f'{score_package_name} has no tools directory.'
        tools = module.tools
        if not hasattr(module.tools, 'ScoreTemplate'):
            return -1, f'{score_package_name}.tools has no ScoreTemplate.py.'
        score_template = tools.ScoreTemplate
        if not hasattr(score_template, 'part_names'):
            message = f'{score_package_name}.ScoreTemplate'
            message += " has no 'part_manifest' property."
            return -1, message
        score_template = module.tools.ScoreTemplate()
        part_manifest = score_template.part_manifest
        return part_manifest

    def _get_repository_root(self):
        if not self.exists():
            return
        if self.wrapper is None:
            path = self
        else:
            path = self.wrapper
        test_scores = self.configuration.test_scores_directory
        if str(self).startswith(str(test_scores)):
            return self.wrapper
        while str(path) != str(path.parts[0]):
            for path_ in path.iterdir():
                if path_.name == '.git':
                    return type(self)(path)
            path = path.parent

    def _get_unadded_asset_paths(self):
        assert self.is_dir()
        paths = []
        root = self.wrapper
        git_status_lines = self._get_git_status_lines()
        for line in git_status_lines:
            line = str(line)
            if line.startswith('?'):
                path = line.strip('?')
                path = path.strip()
                path = root / path
                paths.append(path)
            elif line.startswith('M'):
                path = line.strip('M')
                path = path.strip()
                path = root / path
                paths.append(path)
        paths = [_ for _ in paths]
        return paths

    def _has_pending_commit(self):
        assert self.is_dir()
        command = f'git status {self}'
        with abjad.TemporaryDirectoryChange(directory=self):
            lines = abjad.IOManager.run_command(command)
        clean_lines = []
        for line in lines:
            line = str(line)
            clean_line = line.strip()
            clean_line = clean_line.replace(str(self), '')
            clean_lines.append(clean_line)
        for line in clean_lines:
            if 'Changes not staged for commit:' in line:
                return True
            if 'Changes to be committed:' in line:
                return True
            if 'Untracked files:' in line:
                return True
        
    def _is_git_unknown(self):
        if not self.exists():
            return False
        git_status_lines = self._get_git_status_lines()
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return True
        return False

    def _parse_part_abbreviation(self):
        if self.suffix == '.ly':
            part_abbreviation = None
            with self.open('r') as pointer:
                for line in pointer.readlines():
                    if line.startswith('% part_abbreviation = '):
                        line = line.strip('% part_abbreviation = ')
                        part_abbreviation = eval(line)
                        return part_abbreviation
        elif self.name.endswith('layout.py'):
            part_abbreviation = None
            with self.open('r') as pointer:
                for line in pointer.readlines():
                    if line.startswith('part_abbreviation = '):
                        line = line.strip('part_abbreviation = ')
                        part_abbreviation = eval(line)
                        return part_abbreviation
        else:
            raise TypeError(self)

    def _unadd_added_assets(self):
        paths = []
        paths.extend(self._get_added_asset_paths())
        paths.extend(self._get_modified_asset_paths())
        commands = []
        for path in paths:
            command = f'git reset -- {path}'
            commands.append(command)
        command = ' && '.join(commands)
        with abjad.TemporaryDirectoryChange(directory=path):
            abjad.IOManager.spawn_subprocess(command)

    ### PUBLIC PROPERTIES ###

    @property
    def document_names(self):
        r'''Gets document names in path.

        Returns list of shoutcase strings.
        '''
        if not self.is_build():
            return
        stem = abjad.String(self.name).to_shout_case()
        if not self.is_parts():
            return [stem]
        assert self.is_parts()
        result = []
        part_manifest = self._get_part_manifest()
        for pair in part_manifest:
            part_name, abbreviation = pair
            abbreviation = abjad.String(abbreviation).to_shout_case()
            document_name = f'{stem}_{abbreviation}'
            result.append(document_name)
        return result

    @property
    def scores(self):
        r'''Gets scores directory.

        ..  container:: example

            >>> path = ide.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores
            Path*('/path/to/scores')
            >>> path.scores('red_score', 'red_score', 'etc')
            Path*('/path/to/scores/red_score/red_score/etc')

        Returns package path or none.
        '''
        if getattr(self, '_scores', None) is not None:
            result = self._scores
            result._scores = self._scores
            return result
        for scores in (
            self.configuration.test_scores_directory,
            abjad.abjad_configuration.composer_scores_directory,
            ):
            if str(self).startswith(str(scores)):
                return type(self)(scores)

    ### PUBLIC METHODS ###

    def get_eol_measure_numbers(self):
        r'''Gets EOL measure numbers from BOL measure numbers stored in
        metadata.

        Returns list or none.
        '''
        bol_measure_numbers = self.get_metadatum('bol_measure_numbers')
        if bol_measure_numbers is None:
            return
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        last_measure_number = self.get_metadatum('last_measure_number')
        if last_measure_number is not None:
            eol_measure_numbers.append(last_measure_number)
        return eol_measure_numbers

    def get_header(self):
        r'''Gets menu header.

        Returns string.
        '''
        if self.is_scores():
            return 'Abjad IDE : scores'
        if self.is_external():
            if self.parent.name == abjad.abjad_configuration.composer_library:
                header = 'Abjad IDE : library'
            else:
                header = f'Abjad IDE : {self}'
            if not self.list_paths():
                header += ' (empty)'
            return header
        parts = [self.contents.get_title()]
        if self.is_wrapper():
            parts.append('wrapper')
        elif not self.is_contents():
            parts.extend(self.relative_to(self.contents).parts[:-1])
            parts.append(self.get_identifier())
        if parts and not self.list_paths():
            parts[-1] += ' (empty)'
        return ' : '.join(parts)

    def is_external(self):
        r'''Is true when path does not have form of score package path.

        ..  container:: example

            >>> path = ide.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_external()
            False
            >>> path.contents.is_external()
            False
            >>> path.wrapper.is_external()
            False

            >>> path.scores.is_external()
            True

        ..  container:: example

            >>> ide.Path('/path/to/location').is_external()
            True

        Returns true or false.
        '''
        if (not self.name[0].isalpha() and
            not self.name == '_assets' and
            not self.name == '_segments' and
            not self.parent.name == 'segments'):
            return True
        for scores in (abjad.abjad_configuration.composer_scores_directory,
            self.configuration.test_scores_directory,
            getattr(self, '_scores', None),
            ):
            if str(self) == str(scores):
                return True
            if str(self).startswith(str(scores)):
                return False
        return True

    def is_prototype(self, prototype):
        r'''Is true when path is `prototype`.

        Returns true or false.
        '''
        if prototype is True:
            return True
        if bool(prototype) is False:
            return False
        return self.is_score_package_path(prototype)
