import abjad
import pathlib
from ide.tools.idetools.Configuration import Configuration
from ide.tools.idetools.IOManager import IOManager
from ide.tools.idetools.Session import Session


class Path(pathlib.PosixPath):
    r'''Path.
    '''

    ### CLASS VARIABLES ###

    _configuration = Configuration()

    _example_score_directories = (
        'blue_score',
        'red_score',
        )

    _io_manager = IOManager(session=Session())

    ### CONSTRUCTOR ###

    def __new__(class_, argument):
        arguments = []
        if isinstance(argument, pathlib.Path):
            score_directory = Path._to_score_directory(argument)
            argument = score_directory.name
        if argument in Path._example_score_directories:
            arguments.append(Path._configuration.example_scores_directory)
            arguments.extend(2 * [argument])
        elif argument == 'boilerplate':
            arguments.append(Path._configuration.boilerplate_directory)
        else:
            arguments.append(Path._configuration.composer_scores_directory)
            arguments.extend(2 * [argument])
        self = pathlib.Path.__new__(class_, *arguments)
        return self

    ### PRIVATE METHODS ###

    def _get_metadata(self):
        metadata_py_path = self / '__metadata__.py'
        metadata = None
        if metadata_py_path.is_file():
            file_contents_string = metadata_py_path.read_text()
            try:
                result = self._io_manager.execute_string(
                    file_contents_string,
                    attribute_names=('metadata',),
                    )
                metadata = result[0]
            except SyntaxError:
                message = 'can not interpret metadata py: {}.'
                message = message.format(self._trim(metadata_py_path))
                self._io_manager._display(message)
            except NameError as e:
                raise Exception(repr(metadata_py_path), e)
        metadata = metadata or abjad.TypedOrderedDict()
        return metadata

    def _get_metadatum(self, metadatum_name, default=None):
        metadata = self._get_metadata()
        metadatum = metadata.get(metadatum_name)
        if not metadatum:
            metadatum = default
        return metadatum

    def _get_title_metadatum(self, year=True):
        if year and self._get_metadatum('year'):
            result = '{} ({})'
            result = result.format(
                self._get_title_metadatum(year=False),
                self._get_metadatum('year')
                )
            return result
        else:
            result = self._get_metadatum('title')
            result = result or '(untitled score)'
            return result
        
    @classmethod
    def _is_score_directory(class_, directory, prototype=()):
        if not directory.is_dir():
            return False
        if isinstance(prototype, str):
            prototype = (prototype,)
        if not prototype and class_._to_scores_directory(directory):
            return True
        assert all(isinstance(_, str) for _ in prototype)
        if not class_._to_scores_directory(directory):
            return False
        if 'scores' in prototype:
            if directory == class_._configuration.composer_scores_directory:
                return True
            if directory == class_._configuration.example_scores_directory:
                return True
        scores_directory = class_._to_score_directory(directory, 'scores')
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

    @classmethod
    def _to_score_directory(class_, path, name=None):
        if path.is_dir() and not class_._is_score_directory(path):
            return path
        scores_directory = class_._to_scores_directory(path)
        if name == 'scores':
            return scores_directory
        parts = path.relative_to(scores_directory).parts
        if not parts:
            return
        score_name = parts[0]
        score_name = pathlib.Path(score_name)
        score_directory = scores_directory / score_name / score_name
        if name in ('contents', 'score'):
            pass
        elif name == 'wrapper':
            score_directory = score_directory.parent
        elif name is not None:
            score_directory = score_directory / name
        return score_directory

    @classmethod
    def _to_scores_directory(class_, path):
        string = str(path)
        for scores_directory in (
            class_._configuration.composer_scores_directory,
            class_._configuration.example_scores_directory):
            if string.startswith(str(scores_directory)):
                return scores_directory

    ### PUBLIC PROPERTIES ###

    @property
    def build(self):
        r'''Gets build directory.

        Returns path.
        '''
        return self / 'build'

    @property
    def contents(self):
        r'''Gets contents directory.

        Returns path.
        '''
        return self

    @property
    def distribution(self):
        r'''Gets distribution directory.

        Returns path.
        '''
        return self / 'distribution'

    @property
    def etc(self):
        r'''Gets etc directory.

        Returns path.
        '''
        return self / 'etc'

    @property
    def materials(self):
        r'''Gets materials directory.

        Returns path.
        '''
        return self / 'materials'

    @property
    def segments(self):
        r'''Gets segments directory.

        Returns path.
        '''
        return self / 'segments'

    @property
    def stylesheets(self):
        r'''Gets stylesheets directory.

        Returns path.
        '''
        return self / 'stylesheets'

    @property
    def test(self):
        r'''Gets test directory.

        Returns path.
        '''
        return self / 'test'

    @property
    def tools(self):
        r'''Gets tools directory.

        Returns path.
        '''
        return self / 'tools'

    @property
    def wrapper(self):
        r'''Gets wrapper directory.

        Returns path.
        '''
        return self / 'wrapper'

    ### PUBLIC METHODS ###

    def remove(self):
        r'''Removes path if it exists.

        Returns none.
        '''
        if self.exists():
            self.unlink()
