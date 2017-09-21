import abjad
import os
import pathlib
from ide.tools.idetools.Configuration import Configuration


class Path(abjad.Path):
    r'''Path.
    '''

    ### CLASS VARIABLES ###

    address_characters = {
        '@': 'file',
        '%': 'directory',
        '^': 'Python file',
        '*': 'PDF',
        '+': 'Python file',
        }

    configuration = Configuration()

    test_score_names = (
        'blue_score',
        'red_score',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, argument, scores=None):
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
            self = pathlib.Path.__new__(class_, *arguments)
        if scores is not None:
            scores = type(self)(scores)
        self._scores = scores
        return self

    ### PRIVATE METHODS ###

    def _get_added_asset_paths(self):
        paths = []
        git_status_lines = self._get_git_status_lines()
        for line in git_status_lines:
            line = str(line)
            if line.startswith('A'):
                path = line.strip('A')
                path = path.strip()
                root = self.wrapper()
                path = root / path
                paths.append(path)
        return paths

    def _get_git_status_lines(self):
        with abjad.TemporaryDirectoryChange(directory=self.wrapper()):
            command = f'git status --porcelain {self}'
            return abjad.IOManager.run_command(command)

    def _get_repository_root(self):
        if not self.exists():
            return
        if self.wrapper() is None:
            path = self
        else:
            path = self.wrapper()
        test_scores = self.configuration.test_scores_directory
        if str(self).startswith(str(test_scores)):
            return self.wrapper()
        while str(path) != str(path.parts[0]):
            for path_ in path.iterdir():
                if path_.name == '.git':
                    return type(self)(path)
            path = path.parent

    def _get_unadded_asset_paths(self):
        assert self.is_dir()
        paths = []
        root = self.wrapper()
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
        
    def _is_git_unknown(self):
        if not self.exists():
            return False
        git_status_lines = self._get_git_status_lines()
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return True
        return False

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

    ### PUBLIC METHODS ###

    def full_trim(self, current_directory):
        r'''Gets full trim.
        
        Returns string.
        '''
        if self == current_directory:
            return self.name
        if self.parent == current_directory:
            return self.name
        return self.trim()

    def get_header(self):
        r'''Gets menu header.

        Returns string.
        '''
        if self.is_external():
            if self.parent.name == abjad.abjad_configuration.composer_library:
                header = 'Abjad IDE : library'
            else:
                header = f'Abjad IDE : {self}'
            if not self.list_paths():
                header += ' (empty)'
            return header
        if self.is_scores():
            return 'Abjad IDE : scores'
        parts = [self.contents().get_title()]
        if self.is_wrapper():
            parts.append('wrapper')
        elif not self.is_contents():
            parts.extend(self.relative_to(self.contents()).parts[:-1])
            parts.append(self.get_identifier())
        if parts and not self.list_paths():
            parts[-1] += ' (empty)'
        return ' : '.join(parts)

    def is_external(self):
        r'''Is true when path does not have form of score package path.

        ..  container:: example

            ::

                >>> path = ide.Path('/path/to/location')
                >>> path.is_external()
                True

        Returns true or false.
        '''
        if not self.name[0].isalpha() and not self.name == '_segments':
            return True
        for scores in (abjad.abjad_configuration.composer_scores_directory,
            self.configuration.test_scores_directory,
            getattr(self, '_scores', None),
            ):
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
        return self.is_package_path(prototype)

    def match_paths(self, prefix, pattern):
        r'''Matches paths against `pattern`.

        Returns list.
        '''
        if len(prefix) == 1 and not pattern:
            return []
        if prefix == '%%':
            return []
        path, match = None, True
        if pattern == '<':
            path = self.get_previous_package(cyclic=True)
        elif pattern == '>':
            path = self.get_next_package(cyclic=True)
        elif abjad.mathtools.is_integer_equivalent(pattern):
            segment_number = int(pattern)
            path = self.segment_number_to_path(segment_number)
        if path:
            paths, match = [path], False
        elif len(prefix) == 2:
            paths = self.glob('**/*')
        elif self.is_package_path():
            paths = self.contents().glob('**/*')
        else:
            paths = self.glob('*')
        if prefix.startswith('@'):
            suffixes = self.configuration.editor_suffixes
            paths = [_ for _ in paths if _.suffix in suffixes or _.is_dir()]
        elif prefix.startswith('%'):
            paths = [_ for _ in paths if _.is_dir()]
        elif prefix.startswith('^'):
            paths = [_ for _ in paths if _.suffix == '.py' or _.is_dir()]
        elif prefix.startswith('*'):
            paths = [_ for _ in paths if _.suffix == '.pdf' or _.is_dir()]
        elif prefix.startswith('+'):
            paths = [_ for _ in paths if _.suffix == '.py' or _.is_dir()]
        else:
            raise ValueError(repr(prefix))
        if pattern and match:
            paths_ = []
            strings = [_.get_identifier() for _ in paths]
            for i in self.match_strings(strings, pattern):
                paths_.append(paths[i])
            paths = paths_
        paths_ = []
        for path in paths:
            if prefix[0] in ('@', '^', '+') and path.is_dir():
                path /= 'definition.py'
            elif prefix[0] == '*' and path.is_dir():
                path /= 'illustration.pdf'
            if prefix[0] == '%' or path.is_file():
                path = Path(path)
                paths_.append(path)
            paths = paths_
        if prefix in ('@', '%', '*'):
            paths = paths[:1]
        return paths

    # TODO: move to abjad.String
    @staticmethod
    def match_strings(strings, pattern):
        r'''Matches `pattern` against `strings`.

        ..  container:: example

            ::

                >>> strings = [
                ...     'AcciaccaturaSpecifier.py',
                ...     'AnchorCommand.py',
                ...     'ArpeggiationSpacingSpecifier.py',
                ...     'AttachCommand.py',
                ...     'ChordalSpacingSpecifier.py',
                ...     ]

            ::

                >>> ide.Path.match_strings(strings, 'A')
                []

            ::

                >>> for i in ide.Path.match_strings(strings, 'At'):
                ...     strings[i]
                'AttachCommand.py'

            ::

                >>> for i in ide.Path.match_strings(strings, 'AtC'):
                ...     strings[i]
                'AttachCommand.py'

            ::

                >>> for i in ide.Path.match_strings(strings, 'ASS'):
                ...     strings[i]
                'ArpeggiationSpacingSpecifier.py'

            ::

                >>> for i in ide.Path.match_strings(strings, 'AC'):
                ...     strings[i]
                'AnchorCommand.py'
                'AttachCommand.py'

            ::

                >>> for i in ide.Path.match_strings(strings, '.py'):
                ...     strings[i]
                'AcciaccaturaSpecifier.py'
                'AnchorCommand.py'
                'ArpeggiationSpacingSpecifier.py'
                'AttachCommand.py'
                'ChordalSpacingSpecifier.py'

            ::

                >>> ide.Path.match_strings(strings, '@AC')
                []

        ..  container:: example

            Regression:

            ::

                >>> ide.Path.match_strings(strings, '||')
                []

        Returns string or none.
        '''
        if not pattern:
            return []
        if pattern[0] in Path.address_characters:
            return []
        pattern = abjad.String(pattern)
        indices = []
        for i, string in enumerate(strings):
            if string == pattern:
                indices.append(i)
        strings = [abjad.String(_) for _ in strings]
        if 3 <= len(pattern):
            for i, string in enumerate(strings):
                if string.startswith(pattern):
                    if i not in indices:
                        indices.append(i)
            for i, string in enumerate(strings):
                string = string.strip_diacritics().lower()
                if string.startswith(pattern.lower()):
                    if i not in indices:
                        indices.append(i)
        if len(pattern) <= 1:
            return indices
        if not pattern.islower() or any(_.isdigit() for _ in pattern):
            pattern_words = pattern.delimit_words(separate_caps=True)
            if pattern_words:
                for i, string in enumerate(strings):
                    if (string.startswith(pattern_words[0]) and
                        string.match_word_starts(pattern_words)):
                        if i not in indices:
                            indices.append(i)
                for i, string in enumerate(strings):
                    if string.match_word_starts(pattern_words):
                        if i not in indices:
                            indices.append(i)
        if pattern.islower():
            pattern_characters = list(pattern)
            if pattern_characters:
                for i, string in enumerate(strings):
                    if (string.startswith(pattern_characters[0]) and
                        string.match_word_starts(pattern_characters)):
                        if i not in indices:
                            indices.append(i)
                for i, string in enumerate(strings):
                    if string.match_word_starts(pattern_characters):
                        if i not in indices:
                            indices.append(i)
        if len(pattern) < 3:
            return indices
        for i, string in enumerate(strings):
            if pattern in string.strip_diacritics().lower():
                if i not in indices:
                    indices.append(i)
        return indices

    def scores(self, *names):
        r'''Gets scores directory.

        ..  container:: example

            ::

                >>> path = ide.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )
                >>> path.scores()
                Path*('/path/to/scores')
                >>> path.scores('red_score', 'red_score', 'etc')
                Path*('/path/to/scores/red_score/red_score/etc')

        Returns package path or none.
        '''
        if getattr(self, '_scores', None) is not None:
            result = self._scores
            result._scores = self._scores
            for name in names:
                result /= name
            return result
        for scores in (
            self.configuration.test_scores_directory,
            abjad.abjad_configuration.composer_scores_directory,
            ):
            if str(self).startswith(str(scores)):
                result = type(self)(scores)
                for name in names:
                    result /= name
                return result
