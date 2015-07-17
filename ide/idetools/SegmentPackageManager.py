# -*- encoding: utf-8 -*-
import os
import shutil
import time
from abjad.tools import systemtools
from ide.idetools.ScoreInternalPackageManager import \
    ScoreInternalPackageManager


class SegmentPackageManager(ScoreInternalPackageManager):
    r'''Segment package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(SegmentPackageManager, self)
        superclass.__init__(path=path, session=session)
        optional_files = list(self._optional_files)
        optional_files.extend([
            'illustration.ly',
            'illustration.pdf',
            ])
        self._optional_files = tuple(optional_files)
        required_files = list(self._required_files)
        required_files.extend([
            'definition.py',
            ])
        self._required_files = tuple(required_files)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            name = self._get_metadatum('name')
            name = name or self._space_delimited_lowercase_name
            return name
        name = self._space_delimited_lowercase_name
        configuration = self._configuration
        annotation = configuration._path_to_storehouse_annotation(self._path)
        string = '{} ({})'
        string = string.format(name, annotation)
        return string

    @property
    def _command_to_method(self):
        superclass = super(SegmentPackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'i': self.illustrate_definition_py,
            #
            'ii': self.interpret_illustration_ly,
            'ie': self.edit_illustration_ly,
            'o': self.open_illustration_pdf,
            })
        return result

    @property
    def _definition_py_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _illustration_ly_path(self):
        return os.path.join(self._path, 'illustration.ly')

    @property
    def _illustration_pdf_path(self):
        return os.path.join(self._path, 'illustration.pdf')

    @property
    def _source_paths(self):
        return (
            self._definition_py_path,
            self._illustration_ly_path,
            self._illustration_pdf_path,
            )

    ### PRIVATE METHODS ###

    def _execute_definition_py(self):
        result = self._io_manager.execute_file(
            path = self._definition_py_path,
            attribute_names=('segment_maker',)
            )
        if result and len(result) == 1:
            target = result[0]
            return target

    def _get_previous_segment_manager(self):
        wrangler = self._session._abjad_ide._segment_package_wrangler
        managers = wrangler._list_visible_asset_managers()
        for i, manager in enumerate(managers):
            if manager._path == self._path:
                break
        else:
            message = 'can not find segment package manager.'
            raise Exception(message)
        current_manager_index = i
        if current_manager_index == 0:
            return
        previous_manager_index = current_manager_index - 1
        previous_manager = managers[previous_manager_index]
        return previous_manager

    def _make_definition_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._definition_py_path):
            commands.append(('definition.py - check', 'dc'))
            commands.append(('definition.py - edit', 'de'))
        else:
            commands.append(('definition.py - stub', 'ds'))
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='definition.py',
                )

    def _make_illustration_ly_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_ly_path):
            commands.append(('illustration.ly - edit', 'ie'))
            commands.append(('illustration.ly - interpret', 'ii'))
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='illustration',
                )

    def _make_main_menu(self):
        superclass = super(SegmentPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_definition_py_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        self._make_main_visible_menu_section(menu)
        return menu

    def _make_package(self):
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )

    def _make_main_visible_menu_section(self, menu):
        commands = []
        commands.append(('definition.py - illustrate', 'i'))
        if os.path.isfile(self._illustration_pdf_path):
            commands.append(('illustration.pdf - open', 'o'))
        if commands:
            menu.make_command_section(
                commands=commands,
                is_hidden=False,
                name='main visible section',
                )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_segments = True

    def _update_order_dependent_segment_metadata(self):
        wrangler = self._session._abjad_ide._segment_package_wrangler
        wrangler._update_order_dependent_segment_metadata()

    ### PUBLIC METHODS ###

    def edit_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def edit_illustration_ly(self):
        r'''Opens ``illustration.ly``.

        Returns none.
        '''
        self._open_file(self._illustration_ly_path)

    def illustrate_definition_py(self, dry_run=False):
        r'''Illustrates ``definition.py``.

        Makes ``illustration.ly`` and ``illustration.pdf``.

        Returns none.
        '''
        if not os.path.isfile(self._definition_py_path):
            message = 'File not found: {}.'
            message = message.format(self._definition_py_path)
            self._io_manager._display(message)
            return
        self._update_order_dependent_segment_metadata()
        boilerplate_path = os.path.join(
            self._configuration.abjad_ide_directory,
            'boilerplate',
            '__illustrate_segment__.py',
            )
        illustrate_path = os.path.join(
            self._path,
            '__illustrate_segment__.py',
            )
        candidate_ly_path = os.path.join(
            self._path,
            'illustration.candidate.ly'
            )
        candidate_pdf_path = os.path.join(
            self._path,
            'illustration.candidate.pdf'
            )
        temporary_files = (
            illustrate_path,
            candidate_ly_path,
            candidate_pdf_path,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        illustration_ly_path = os.path.join(
            self._path,
            'illustration.ly',
            )
        illustration_pdf_path = os.path.join(
            self._path,
            'illustration.pdf',
            )
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._definition_py_path)
            outputs.append((illustration_ly_path, illustration_pdf_path))
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(boilerplate_path, illustrate_path)
            previous_segment_manager = self._get_previous_segment_manager()
            if previous_segment_manager is None:
                statement = 'previous_segment_metadata = None'
            else:
                score_name = self._session.current_score_directory
                score_name = os.path.basename(score_name)
                previous_segment_name = previous_segment_manager._path
                previous_segment_name = os.path.basename(previous_segment_name)
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_segment_metadata'
                statement = statement.format(score_name, previous_segment_name)
            self._replace_in_file(
                illustrate_path,
                'PREVIOUS_SEGMENT_METADATA_IMPORT_STATEMENT',
                statement,
                )
            with self._io_manager._silent():
                start_time = time.time()
                result = self._io_manager.interpret_file(
                    illustrate_path,
                    strip=False,
                    )
                stop_time = time.time()
                total_time = stop_time - start_time
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            message = 'total time: {} seconds.'
            message = message.format(int(total_time))
            self._io_manager._display(message)
            if not os.path.exists(illustration_pdf_path):
                messages = []
                messages.append('Wrote ...')
                tab = self._io_manager._tab
                if os.path.exists(candidate_ly_path):
                    shutil.move(candidate_ly_path, illustration_ly_path)
                    messages.append(tab + illustration_ly_path)
                if os.path.exists(candidate_pdf_path):
                    shutil.move(candidate_pdf_path, illustration_pdf_path)
                    messages.append(tab + illustration_pdf_path)
                self._io_manager._display(messages)
            else:
                result = systemtools.TestManager.compare_files(
                candidate_pdf_path,
                illustration_pdf_path,
                )
                messages = self._make_candidate_messages(
                    result, candidate_pdf_path, illustration_pdf_path)
                self._io_manager._display(messages)
                if result:
                    message = 'preserved {}.'.format(illustration_pdf_path)
                    self._io_manager._display(message)
                    return
                else:
                    message = 'overwrite existing PDF with candidate PDF?'
                    result = self._io_manager._confirm(message=message)
                    if self._session.is_backtracking or not result:
                        return
                    try:
                        shutil.move(candidate_ly_path, illustration_ly_path)
                    except IOError:
                        pass
                    try:
                        shutil.move(candidate_pdf_path, illustration_pdf_path)
                    except IOError:
                        pass

    def open_illustration_pdf(self):
        r'''Opens ``illustration.pdf``.

        Returns none.
        '''
        self._open_file(self._illustration_pdf_path)

    def write_stub_definition_py(self):
        r'''Writes stub ``definition.py``.

        Returns none.
        '''
        messages = []
        message = 'will write stub to {}.'
        message = message.format(self._definition_py_path)
        messages.append(message)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        source_path = os.path.join(
            self._configuration.abjad_ide_directory,
            'boilerplate',
            'definition.py',
            )
        destination_path = self._definition_py_path
        shutil.copyfile(source_path, destination_path)