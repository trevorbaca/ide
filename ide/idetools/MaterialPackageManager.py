# -*- encoding: utf-8 -*-
import copy
import os
import shutil
from abjad.tools import datastructuretools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.idetools.ScoreInternalPackageManager import \
    ScoreInternalPackageManager


class MaterialPackageManager(ScoreInternalPackageManager):
    r'''Material package manager.


    ..  container:: example

        ::

            >>> import os
            >>> configuration = ide.idetools.Configuration()
            >>> session = ide.idetools.Session()
            >>> path = os.path.join(
            ...     configuration.example_score_packages_directory,
            ...     'red_example_score',
            ...     'materials',
            ...     'performer_inventory',
            ...     )
            >>> manager = ide.idetools.MaterialPackageManager(
            ...     path=path,
            ...     session=session,
            ...     )
            >>> manager
            MaterialPackageManager('.../materials/performer_inventory')

    '''

    ### INTIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(MaterialPackageManager, self)
        superclass.__init__(path=path, session=session)
        optional_files = list(self._optional_files)
        optional_files.extend([
            '__illustrate__.py',
            'illustration.ly',
            'illustration.pdf',
            'maker.py',
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
        breadcrumb = self._space_delimited_lowercase_name
        if not self._session.is_in_library and not self._session.is_in_score:
            annotation = self._path_to_annotation(self._path)
            breadcrumb = '{} - {}'.format(annotation, breadcrumb)
        return breadcrumb

    @property
    def _command_to_method(self):
        superclass = super(MaterialPackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'dc': self.check_definition_py,
            'de': self.edit_definition_py,
            'ds': self.write_stub_definition_py,
            #
            'le': self.edit_illustrate_py,
            'ls': self.write_stub_illustrate_py,
            #
            'ii': self.interpret_illustration_ly,
            'ie': self.edit_illustration_ly,
            'io': self.open_illustration_pdf,
            })
        return result

    @property
    def _definition_py_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _handlertools_import_statement(self):
        return 'from abjad.tools import handlertools'

    @property
    def _illustrate_py_path(self):
        return os.path.join(self._path, '__illustrate__.py')

    @property
    def _illustration_ly_path(self):
        return os.path.join(self._path, 'illustration.ly')

    @property
    def _illustration_pdf_path(self):
        return os.path.join(self._path, 'illustration.pdf')

    @property
    def _maker_py_path(self):
        return os.path.join(self._path, 'maker.py')

    @property
    def _score_package_manager(self):
        from ide import idetools
        score_path = self._configuration._path_to_score_path(self._path)
        return idetools.ScorePackageManager(
            path=score_path,
            session=self._session,
            )

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
            attribute_names=(self._package_name,)
            )
        if result and len(result) == 1:
            target = result[0]
            return target

    def _get_storage_format(self, expr):
        if hasattr(expr, '_storage_format_specification'):
            return format(expr, 'storage')
        return repr(expr)

    def _make_definition_py_menu_section(self, menu):
        name = 'definition.py'
        commands = []
        commands.append(('definition.py - check', 'dc'))
        commands.append(('definition.py - edit', 'de'))
        commands.append(('definition.py - stub', 'ds'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='definition.py',
            )

    def _make_definition_target_lines(self, target):
        if hasattr(target, '_storage_format_specification'):
            lines = format(target, 'storage').splitlines()
        else:
            lines = [repr(target)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self._package_name, lines[0])
        if ' makers.' in lines[0]:
            module = target.__class__.__module__
            parts = module.split('.')
            index = parts.index('makers')
            storehouse = parts[index-1]
            line = lines[0]
            unqualified = ' makers.'
            qualified = ' {}.makers.'.format(storehouse)
            line = line.replace(unqualified, qualified)
            lines[0] = line
        return lines

    def _make_illustrate_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustrate_py_path):
            is_hidden = False
            string = '__illustrate__.py - edit'
            commands.append((string, 'le'))
            string = '__illustrate__.py - stub'
            commands.append((string, 'ls'))
        else:
            is_hidden = True
            string = '__illustrate__.py - stub'
            commands.append((string, 'ls'))
        menu.make_command_section(
            is_hidden=is_hidden,
            commands=commands,
            name='__illustrate__.py',
            )

    def _make_illustration_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_ly_path):
            commands.append(('illustration.ly - interpret', 'ii'))
            commands.append(('illustration.ly - edit', 'ie'))
        if os.path.isfile(self._illustration_pdf_path):
            commands.append(('illustration.pdf - open', 'io'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='illustration.pdf',
                )

    def _make_main_menu(self):
        superclass = super(MaterialPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_illustrate_py_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_definition_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_package(self):
        metadata = datastructuretools.TypedOrderedDict()
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )
            self._write_metadata_py(metadata)
            self.write_stub_definition_py()

    def _rename_interactively(
        self,
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        getter = self._io_manager._make_getter()
        getter.append_identifier('enter new package name', allow_spaces=True)
        new_package_name = getter._run()
        if self._session.is_backtracking or new_package_name is None:
            return
        new_package_name = stringtools.to_snake_case(new_package_name)
        base_name = os.path.basename(self._path)
        new_directory = self._path.replace(
            base_name,
            new_package_name,
            )
        messages = []
        messages.append('will change ...')
        messages.append(' FROM: {}'.format(self._path))
        messages.append('   TO: {}'.format(new_directory))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._rename(new_directory)
        if not os.path.exists(new_directory):
            return
        for directory_entry in sorted(os.listdir(new_directory)):
            if directory_entry.endswith('.py'):
                path = os.path.join(new_directory, directory_entry)
                result = os.path.splitext(base_name)
                old_package_name, extension = result
                self._replace_in_file(
                    path,
                    old_package_name,
                    new_package_name,
                    )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_materials = True

    ### PUBLIC METHODS ###

    def edit_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def edit_illustrate_py(self):
        r'''Edits ``__illustrate.py__``.

        Returns none.
        '''
        self._io_manager.edit(self._illustrate_py_path)

    def edit_illustration_ly(self):
        r'''Opens ``illustration.ly``.

        Returns none.
        '''
        self._io_manager.open_file(self._illustration_ly_path)

    # TODO: refactor with SegmentPackageManager.illustrate_definition_py()
    # TODO: maybe change to self.illustration_definition_py()
#    def illustrate_output_py(self):
#        r'''Illustrates ``output.py``.
#
#        Makes ``illustration.pdf`` and ``illustration.ly``.
#
#        Returns none.
#        '''
#        if os.path.isfile(self._illustrate_py_path):
#            boilerplate_name = '__illustrate_material_2__.py'
#        else:
#            boilerplate_name = '__illustrate_material_1__.py'
#        boilerplate_path = os.path.join(
#            self._configuration.abjad_ide_directory,
#            'boilerplate',
#            boilerplate_name,
#            )
#        illustrate_path = os.path.join(
#            self._path,
#            '__illustrate_material__.py',
#            )
#        candidate_ly_path = os.path.join(
#            self._path, 
#            'illustration.candidate.ly'
#            )
#        candidate_pdf_path = os.path.join(
#            self._path, 
#            'illustration.candidate.pdf'
#            )
#        temporary_files = (
#            illustrate_path, 
#            candidate_ly_path,
#            candidate_pdf_path,
#            )
#        for path in temporary_files:
#            if os.path.exists(path):
#                os.remove(path)
#        illustration_ly_path = os.path.join(
#            self._path,
#            'illustration.ly',
#            )
#        illustration_pdf_path = os.path.join(
#            self._path,
#            'illustration.pdf',
#            )
#        with systemtools.FilesystemState(remove=temporary_files):
#            shutil.copyfile(boilerplate_path, illustrate_path)
#            self._replace_in_file(
#                illustrate_path, 
#                'OUTPUT_OBJECT', 
#                self._package_name,
#                )
#            with self._io_manager._silent():
#                result = self._io_manager.interpret_file(illustrate_path)
#            stdout_lines, stderr_lines = result
#            if stderr_lines:
#                self._io_manager._display(stderr_lines, capitalize=False)
#                return
#            messages = []
#            tab = self._io_manager._tab
#            if not os.path.exists(illustration_pdf_path):
#                shutil.move(candidate_pdf_path, illustration_pdf_path)
#                shutil.move(candidate_ly_path, illustration_ly_path)
#                tab = self._io_manager._tab
#                messages.append('Wrote ...')
#                messages.append(tab + illustration_ly_path)
#                messages.append(tab + illustration_pdf_path)
#                self._io_manager._display(messages)
#            else:
#                result = systemtools.TestManager.compare_files(
#                candidate_pdf_path,
#                illustration_pdf_path,
#                )
#                if result:
#                    messages.append('the files ...')
#                    messages.append(tab + candidate_pdf_path)
#                    messages.append(tab + illustration_pdf_path)
#                    messages.append('... compare the same.')
#                    self._io_manager._display(messages)
#                    message = 'Preserved {}.'.format(illustration_pdf_path)
#                    self._io_manager._display(message)
#                    return
#                else:
#                    messages.append('the files ...')
#                    messages.append(tab + candidate_pdf_path)
#                    messages.append(tab + illustration_pdf_path)
#                    messages.append('... compare differently.')
#                    self._io_manager._display(messages)
#                    message = 'overwrite existing PDF with candidate PDF?'
#                    result = self._io_manager._confirm(message=message)
#                    if self._session.is_backtracking or not result:
#                        return
#                    shutil.move(candidate_pdf_path, illustration_pdf_path)
#                    shutil.move(candidate_ly_path, illustration_ly_path)

    def open_illustration_pdf(self):
        r'''Opens ``illustration.pdf``.

        Returns none.
        '''
        self._io_manager.open_file(self._illustration_pdf_path)

    def write_definition_py(
        self,
        import_statements=None,
        target=None,
        target_lines=None,
        ):
        r'''Writes ``definition.py``.

        Returns none.
        '''
        assert isinstance(import_statements, list), repr(import_statements)
        assert isinstance(target_lines, list), repr(target_lines)
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.extend(import_statements)
        lines.append('')
        lines.append('')
        lines.extend(target_lines)
        contents = '\n'.join(lines)
        self._io_manager.write(self._definition_py_path, contents)
        message = 'wrote {} to {}.'
        name = type(target).__name__
        message = message .format(name, self._definition_py_path)
        self._session._pending_redraw = True
        self._session._after_redraw_message = message

    # TODO: replace with boilerplate
    def write_stub_definition_py(self):
        r'''Writes stub ``definition.py``.

        Returns none.
        '''
        message = 'will write stub to {}.'
        message = message.format(self._definition_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('')
        lines.append('')
        line = '{} = None'.format(self._package_name)
        lines.append(line)
        contents = '\n'.join(lines)
        with open(self._definition_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        message = 'wrote stub to {}.'.format(self._definition_py_path)
        self._io_manager._display(message)

    # TODO: replace with boilerplate
    # TODO: maybe eliminate altogether?
    def write_stub_illustrate_py(self):
        r'''Writes stub ``__illustrate.py__``.

        Returns none.
        '''
        message = 'will write stub to {}.'
        message = message.format(self._illustrate_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        lines = []
        lines.append(self._abjad_import_statement)
        line = 'from output import {}'
        line = line.format(self._package_name)
        lines.append(line)
        lines.append('')
        lines.append('')
        line = 'triple = scoretools.make_piano_score_from_leaves({})'
        line = line.format(self._package_name)
        lines.append(line)
        line = 'score, treble_staff, bass_staff = triple'
        lines.append(line)
        line = 'illustration = lilypondfiletools.'
        line += 'make_basic_lilypond_file(score)'
        lines.append(line)
        contents = '\n'.join(lines)
        with open(self._illustrate_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        message = 'wrote stub to {}.'
        message = message.format(self._illustrate_py_path)
        self._io_manager._display(message)