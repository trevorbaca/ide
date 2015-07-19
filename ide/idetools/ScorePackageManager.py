# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import indicatortools
from abjad.tools import systemtools
from ide.idetools.PackageManager import PackageManager


class ScorePackageManager(PackageManager):
    r'''Score package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ScorePackageManager, self)
        superclass.__init__(path=path, session=session)
        self._annotate_year = True
        self._include_asset_name = False
        optional_directories = list(self._optional_directories)
        optional_directories.extend([
            'etc',
            ])
        self._optional_directories = tuple(optional_directories)
        required_directories = list(self._required_directories)
        required_directories.extend([
            'build',
            'distribution',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            ])
        self._required_directories = tuple(required_directories)
        required_files = list(self._required_files)
        makers_init_py = os.path.join('makers', '__init__.py')
        materials_init_py = os.path.join('materials', '__init__.py')
        segments_init_py = os.path.join('segments', '__init__.py')
        required_files.extend([
            makers_init_py,
            materials_init_py,
            segments_init_py,
            ])
        self._required_files = tuple(required_files)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        annotated_title = self._get_title(year=True)
        return annotated_title

    @property
    def _command_to_method(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'so': self.open_score_pdf,
            'pw': self.write_enclosing_artifacts,
            })
        return result

    @property
    def _inner_path(self):
        return os.path.join(self._outer_path, self._package_name)

    @property
    def _outer_path(self):
        if self._path.startswith(
            self._configuration.user_score_packages_directory):
            return os.path.join(
                self._configuration.user_score_packages_directory,
                self._package_name
                )
        else:
            return os.path.join(
                self._configuration.example_score_packages_directory,
                self._package_name
                )

    ### PRIVATE METHODS ###

    def _copy_boilerplate(self, file_name, replacements=None):
        replacements = replacements or {}
        source_path = os.path.join(
            self._configuration.abjad_ide_directory,
            'boilerplate',
            file_name,
            )
        destination_path = os.path.join(
            self._outer_path,
            file_name,
            )
        shutil.copyfile(source_path, destination_path)
        for old in replacements:
            new = replacements[old]
            self._replace_in_file(destination_path, old, new)

    def _enter_run(self):
        superclass = super(ScorePackageManager, self)
        superclass._enter_run()
        self._session._last_score_path = self._path

    def _exit_run(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._exit_run()
        if self._session.is_backtracking_to_score:
            self._session._is_backtracking_to_score = False
            result = False
        elif self._session.is_autonavigating_within_score:
            if self._session.is_backtracking_to_all_scores:
                result = True
            else:
                result = False
        return result

    def _get_build_directory(self):
        return os.path.join(
            self._path,
            'build',
            )

    def _get_distribution_directory(self):
        return os.path.join(
            self._path,
            'distribution',
            )

    def _get_initializer_file_lines(self, missing_file):
        lines = []
        lines.append(self._configuration.unicode_directive)
        if 'materials' in missing_file or 'makers' in missing_file:
            lines.append('from abjad.tools import systemtools')
            lines.append('')
            line = 'systemtools.ImportManager.import_material_packages('
            lines.append(line)
            lines.append('    __path__[0],')
            lines.append('    globals(),')
            lines.append('    )')
        elif 'segments' in missing_file:
            pass
        else:
            lines.append('import makers')
            lines.append('import materials')
            lines.append('import segments')
        return lines

    def _get_makers_directory(self):
        return os.path.join(
            self._path,
            'makers',
            )

    def _get_materials_directory(self):
        return os.path.join(
            self._path,
            'materials',
            )

    def _get_segments_directory(self):
        return os.path.join(
            self._path,
            'segments',
            )

    def _get_stylesheets_directory(self):
        return os.path.join(
            self._path,
            'stylesheets',
            )

    def _get_title(self, year=False):
        if year and self._get_metadatum('year'):
            result = '{} ({})'
            result = result.format(
                self._get_title(),
                self._get_metadatum('year')
                )
            return result
        else:
            return self._get_metadatum('title') or '(untitled score)'

    def _get_top_level_directories(self):
        return (
            self._get_build_directory(),
            self._get_distribution_directory(),
            self._get_makers_directory(),
            self._get_materials_directory(),
            self._get_segments_directory(),
            self._get_stylesheets_directory(),
            )

    def _get_top_level_wranglers(self):
        return (
            self._session._abjad_ide._build_file_wrangler,
            self._session._abjad_ide._distribution_file_wrangler,
            self._session._abjad_ide._maker_file_wrangler,
            self._session._abjad_ide._material_package_wrangler,
            self._session._abjad_ide._segment_package_wrangler,
            self._session._abjad_ide._stylesheet_wrangler,
            )

    def _make_main_menu(self):
        superclass = super(ScorePackageManager, self)
        menu = superclass._make_main_menu()
        self._make_init_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_package_menu_section(menu)
        return menu

    def _make_package(self):
        assert not os.path.exists(self._outer_path)
        os.mkdir(self._outer_path)
        with self._io_manager._silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )
        old_path = self._outer_path
        temporary_path = os.path.join(
            os.path.dirname(self._outer_path),
            '_TEMPORARY_SCORE_PACKAGE',
            )
        shutil.move(old_path, temporary_path)
        shutil.move(temporary_path, self._inner_path)
        self._write_enclosing_artifacts()

    def _make_package_menu_section(self, menu):
        superclass = super(ScorePackageManager, self)
        commands = superclass._make_package_menu_section(
            menu, commands_only=True)
        commands.append(('package - score.pdf - open', 'so'))
        commands.append(('package - write enclosing artifacts', 'pw'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='package',
            )

    def _parse_paper_dimensions(self):
        string = self._get_metadatum('paper_dimensions') or '8.5 x 11 in'
        parts = string.split()
        assert len(parts) == 4
        width, _, height, units = parts
        width = eval(width)
        height = eval(height)
        return width, height, units

    def _write_enclosing_artifacts(self):
        self._path = self._inner_path
        self._copy_boilerplate('README.md')
        self._copy_boilerplate('requirements.txt')
        self._copy_boilerplate('setup.cfg')
        replacements = {
            'COMPOSER_EMAIL': self._configuration.composer_email,
            'COMPOSER_FULL_NAME': self._configuration.composer_full_name,
            'GITHUB_USERNAME': self._configuration.github_username,
            'PACKAGE_NAME': self._package_name,
            }
        self._copy_boilerplate('setup.py', replacements=replacements)

    ### PUBLIC METHODS ###

    def open_score_pdf(self, dry_run=False):
        r'''Opens ``score.pdf``.

        Returns none.
        '''
        with self._io_manager._make_interaction(dry_run=dry_run):
            file_name = 'score.pdf'
            directory = self._get_distribution_directory()
            manager = self._io_manager._make_package_manager(directory)
            path = manager._get_file_path_ending_with(file_name)
            if not path:
                directory = self._get_build_directory()
                manager = self._io_manager._make_package_manager(directory)
                path = manager._get_file_path_ending_with(file_name)
            if dry_run:
                inputs, outputs = [], []
                if path:
                    inputs = [path]
                return inputs, outputs
            if path:
                self._io_manager.open_file(path)
            else:
                message = "no score.pdf file found"
                message += ' in either distribution/ or build/ directories.'
                self._io_manager._display(message)

    def write_enclosing_artifacts(self):
        r'''Writes README.md, requirements.txt, setup.cfg and setup.py
        to enclosing directory of score package.

        Returns none.
        '''
        if not os.path.exists(self._inner_path):
            message = 'score package must be structured'
            message += ' with enclosing directory.'
            self._io_manager._display(message)
            return
        self._write_enclosing_artifacts()
        message = 'wrote enclosing artifacts.'
        self._io_manager._display(message)