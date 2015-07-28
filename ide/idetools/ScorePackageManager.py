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
        self._asset_identifier = 'score package manager'
        self._breadcrumb_callback = self._get_title
        self._directory_names = (
            'build',
            'distribution',
            'etc',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            )
        self._include_asset_name = False
        self._optional_directories = (
            '__pycache__',
            'etc',
            'test',
            )
        self._package_creation_callback = \
            self._make_score_into_installable_package
        self._required_directories = (
            'build',
            'distribution',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            os.path.join('makers', '__init__.py'),
            os.path.join('materials', '__init__.py'),
            os.path.join('segments', '__init__.py'),
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

    def _make_main_menu(self):
        superclass = super(ScorePackageManager, self)
        menu = superclass._make_main_menu()
        self._make_package_menu_section(menu)
        return menu

    def _make_package_menu_section(self, menu):
        superclass = super(ScorePackageManager, self)
        commands = superclass._make_package_menu_section(
            menu, commands_only=True)
        commands.append(('open score.pdf', 'so'))
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