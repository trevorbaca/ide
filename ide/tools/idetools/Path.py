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
        '^': 'source file',
        '*': 'PDF',
        '+': 'test file',
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
                root = self.wrapper
                path = root / path
                paths.append(path)
        return paths

    def _get_git_status_lines(self):
        with abjad.TemporaryDirectoryChange(directory=self.wrapper):
            command = f'git status --porcelain {self}'
            return abjad.IOManager.run_command(command)

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

    ### PUBLIC PROPERTIES ###

    @property
    def scores(self):
        r'''Gets scores directory.

        ..  container:: example

            ::

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

    def collect_paths(self, prefix, pattern=None):
        r'''Collects `prefix` paths that match `pattern`.

        ..  container:: example

            In segments directory:

            ::

                >>> directory = ide.Path('red_score').segments

            Missing pattern:

            ::

                >>> directory.collect_paths('@')
                []

            
            Unique local match (in current directory):

            ::

                >>> for path in directory.collect_paths('@', '__init'):
                ...     path.trim()
                ...
                'red_score/segments/__init__.py'

            Unique remote match (elsewhere in score):

            ::

                >>> for path in directory.collect_paths('@', 'ST'):
                ...     path.trim()
                ...
                'red_score/tools/ScoreTemplate.py'

            Neither local nor remote unique match; so all matches scorewide
            (for error messaging):

            ::

                >>> for path in directory.collect_paths('@', 'def'):
                ...     path.trim()
                ...
                'red_score/materials/magic_numbers/definition.py'
                'red_score/materials/performers/definition.py'
                'red_score/materials/ranges/definition.py'
                'red_score/materials/tempi/definition.py'
                'red_score/materials/time_signatures/definition.py'
                'red_score/segments/segment_01/definition.py'
                'red_score/segments/segment_02/definition.py'
                'red_score/segments/segment_03/definition.py'

            No matches anywhere in score:

            ::

                >>> directory.collect_paths('@', 'asdf')
                []

            All editable nonprivate files in current tree:

            ::

                >>> for path in directory.collect_paths('@@'):
                ...     path.trim()
                ...
                'red_score/segments/segment_01/definition.py'
                'red_score/segments/segment_02/definition.py'
                'red_score/segments/segment_03/definition.py'
                'red_score/segments/segment_01/illustration.ly'
                'red_score/segments/segment_02/illustration.ly'
                'red_score/segments/segment_03/illustration.ly'

            All matches in current tree:

            ::

                >>> for path in directory.collect_paths('@@', '__init'):
                ...     path.trim()
                ...
                'red_score/segments/__init__.py'
                'red_score/segments/segment_01/__init__.py'
                'red_score/segments/segment_02/__init__.py'
                'red_score/segments/segment_03/__init__.py'

            ::

                >>> for path in directory.collect_paths('@@', 'def'):
                ...     path.trim()
                ...
                'red_score/segments/segment_01/definition.py'
                'red_score/segments/segment_02/definition.py'
                'red_score/segments/segment_03/definition.py'

            No match in current tree:

            ::

                >>> directory.collect_paths('@@', 'ST')
                []

            ::

                >>> directory.collect_paths('@@', 'asdf')
                []

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
        elif len(prefix) == 1 and self.is_package_path():
            paths = self.contents.glob('**/*')
        else:
            paths = self.glob('**/*')
        if prefix.startswith('@'):
            suffixes = self.configuration.editor_suffixes
            paths = [_ for _ in paths if _.suffix in suffixes or _.is_dir()]
        elif prefix.startswith('%'):
            paths = [_ for _ in paths if _.is_dir()]
        elif prefix.startswith('^'):
            paths = [
                _ for _ in paths
                if (_.suffix == '.py' or _.is_dir()) and
                not _.name.startswith('test_')
                ]
        elif prefix.startswith('*'):
            paths = [_ for _ in paths if _.suffix == '.pdf' or _.is_dir()]
        elif prefix.startswith('+'):
            paths = [
                _ for _ in paths
                if _.name.startswith('test_') and _.suffix == '.py'
                ]
        else:
            raise ValueError(repr(prefix))
        if not pattern:
            paths = [_ for _ in paths if not _.name.startswith('_')]
        if pattern and match:
            strings = [_.get_identifier() for _ in paths]
            indices = abjad.String.match_strings(strings, pattern)
            paths = abjad.Sequence(paths).retain(indices)
        result = []
        for path in paths:
            if prefix[0] in ('@', '^', '+') and path.is_dir():
                path /= 'definition.py'
            elif prefix[0] == '*' and path.is_dir():
                path /= 'illustration.pdf'
            if path.is_file() or prefix == '%':
                path = Path(path)
                if path not in result:
                    result.append(path)
        if len(prefix) == 1 and 1 < len(result):
            children = [_ for _ in result if _.parent == self]
            if len(children) == 1:
                result = children
        return result

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
