import abjad
import os
import pathlib
import shutil
from ide.tools.idetools.Configuration import Configuration
from ide.tools.idetools.IOManager import IOManager
from ide.tools.idetools.Session import Session


class Path(pathlib.PosixPath):
    r'''Path.
    '''

    ### CLASS VARIABLES ###

    _configuration = Configuration()

    _example_score_names = (
        'blue_score',
        'red_score',
        )

    _io_manager = IOManager(session=Session())

    ### CONSTRUCTOR ###

    def __new__(class_, argument):
        if isinstance(argument, pathlib.Path):
            self = pathlib.Path.__new__(class_, argument)
            return self
        assert isinstance(argument, str), repr(argument)
        if os.sep in argument:
            self = pathlib.Path.__new__(class_, argument)
            return self
        arguments = []
        if argument in Path._example_score_names:
            arguments.append(Path._configuration.example_scores_directory)
            arguments.extend(2 * [argument])
        elif argument == 'boilerplate':
            arguments.append(Path._configuration.boilerplate_directory)
        elif argument == 'example_scores':
            arguments.append(Path._configuration.example_scores_directory)
        else:
            arguments.append(Path._configuration.composer_scores_directory)
            arguments.extend(2 * [argument])
        self = pathlib.Path.__new__(class_, *arguments)
        return self

    ### PRIVATE METHODS ###

    def _add_metadatum(self, name, value):
        assert ' ' not in name, repr(name)
        metadata = self._get_metadata()
        metadata[name] = value
        self._write_metadata_py(metadata)

    def _clear_view(self):
        self._add_metadatum('view_name', None)

    def _coerce_name(self, name):
        dash_case_prototype = ('build subdirectory', 'distribution', 'etc')
        package_prototype = ('scores', 'materials', 'segments')
        if self._is_score_directory('scores'):
            name = self._to_package_name(name)
        elif self._is_score_directory('build'):
            name = self._to_build_subdirectory_name(name)
        elif self._is_score_directory(dash_case_prototype):
            name = self._to_dash_case_file_name(name)
        elif self._is_score_directory('tools'):
            if name[0].isupper():
                name = self._to_classfile_name(name)
            else:
                name = self._to_snake_case_file_name(name)
        elif self._is_score_directory('wrapper'):
            pass
        elif self._is_score_directory(package_prototype):
            name = self._to_package_name(name)
        elif self._is_score_directory('stylesheets'):
            name = self._to_stylesheet_name(name)
        elif self._is_score_directory('test'):
            name = self._to_test_file_name(name)
        return name

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

    def _is_score_directory(self, prototype=()):
        if not self.is_dir():
            return False
        if isinstance(prototype, str):
            prototype = (prototype,)
        if not prototype and self._to_scores_directory(self):
            return True
        assert all(isinstance(_, str) for _ in prototype)
        if not self._to_scores_directory(self):
            return False
        if 'scores' in prototype:
            if self == self._configuration.composer_scores_directory:
                return True
            if self == self._configuration.example_scores_directory:
                return True
        scores_directory = self._to_score_directory(self, 'scores')
        if 'wrapper' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = self.parts
            if len(parts) == scores_directory_parts_count + 1:
                return True
        if 'contents' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = self.parts
            if len(parts) == scores_directory_parts_count + 2:
                if parts[-1] == parts[-2]:
                    return True
        if 'build subdirectory' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = self.parts
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'build' and not parts[-1] == '_segments':
                    return True
        if 'material' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = self.parts
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'materials':
                    return True
        if 'segment' in prototype and scores_directory:
            scores_directory_parts_count = len(scores_directory.parts)
            parts = self.parts
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'segments':
                    return True
        if self.name not in (
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
        if self.name in prototype:
            return True
        return False

    @staticmethod
    def _to_build_subdirectory_name(name):
        assert isinstance(name, str), repr(name)
        name = name.lower()
        name = name.replace(' ', '-')
        name = name.replace('_', '-')
        return name

    def _to_classfile_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = Path(name).stem
        name = abjad.String(name).to_upper_camel_case()
        name = name + '.py'
        assert self._is_classfile_name(name), repr(name)
        return name

    def _to_dash_case_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = name.lower()
        name = Path(name).stem
        suffix = Path(name).suffix
        name = abjad.String(name).to_dash_case()
        suffix = suffix or '.txt'
        name = name + suffix
        assert self._is_dash_case_file_name(name), repr(name)
        return name

    def _to_package_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = name.lower()
        name = Path(name).name
        name = abjad.String(name).to_snake_case()
        assert self._is_package_name(name), repr(name)
        return name
        
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

    def _to_snake_case_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = name.lower()
        name = Path(name).stem
        name = abjad.String(name).to_snake_case()
        name = name + '.py'
        assert self._is_public_python_file_name(name), repr(name)
        return name

    def _to_stylesheet_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = name.lower()
        name = Path(name).stem
        name = abjad.String(name).to_dash_case()
        name = name + '.ily'
        assert self._is_stylesheet_name(name), repr(name)
        return name

    def _to_test_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = abjad.String(name).strip_diacritics()
        name = name.lower()
        name = Path(name).stem
        name = abjad.String(name).to_snake_case()
        if not name.startswith('test_'):
            name = 'test_' + name
        name = name + '.py'
        assert self._is_test_file_name(name), repr(name)
        return name

    def _write_metadata_py(self, metadata):
        metadata_py_path = self / '__metadata__.py'
        lines = []
        lines.append('import abjad')
        lines.append('')
        lines.append('')
        text = '\n'.join(lines)
        metadata = abjad.TypedOrderedDict(metadata)
        items = list(metadata.items())
        items.sort()
        metadata = abjad.TypedOrderedDict(items)
        metadata_lines = format(metadata, 'storage')
        metadata_lines = 'metadata = {}'.format(metadata_lines)
        text = text + '\n' + metadata_lines + '\n'
        metadata_py_path.write_text(text)

    ### PUBLIC PROPERTIES ###

    @property
    def build(self):
        r'''Gets build directory.

        Returns path.
        '''
        return self.contents / 'build'

    @property
    def contents(self):
        r'''Gets contents directory.

        Returns path.
        '''
        return type(self)(self._to_score_directory(self, 'contents'))

    @property
    def distribution(self):
        r'''Gets distribution directory.

        Returns path.
        '''
        return self.contents / 'distribution'

    @property
    def etc(self):
        r'''Gets etc directory.

        Returns path.
        '''
        return self.contents / 'etc'

    @property
    def is_build_subdirectory(self):
        '''Is true when path is build subdirectory.

        Returns true or false.
        '''
        return self.parent.name == 'build'

    @property
    def materials(self):
        r'''Gets materials directory.

        Returns path.
        '''
        return self.contents / 'materials'

    @property
    def segments(self):
        r'''Gets segments directory.

        Returns path.
        '''
        return self.contents / 'segments'

    @property
    def stylesheets(self):
        r'''Gets stylesheets directory.

        Returns path.
        '''
        return self.contents / 'stylesheets'

    @property
    def test(self):
        r'''Gets test directory.

        Returns path.
        '''
        return self.contents / 'test'

    @property
    def tools(self):
        r'''Gets tools directory.

        Returns path.
        '''
        return self.contents / 'tools'

    @property
    def wrapper(self):
        r'''Gets wrapper directory.

        Returns path.
        '''
        return type(self)(self.contents).parent

    ### PUBLIC METHODS ###

    def remove(self):
        r'''Removes path if it exists.

        Returns none.
        '''
        if self.is_file():
            self.unlink()
        elif self.is_dir():
            shutil.rmtree(str(self))
