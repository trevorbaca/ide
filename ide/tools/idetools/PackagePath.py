import abjad
import shutil
from abjad import abjad_configuration


class PackagePath(abjad.PackagePath):
    r'''Packge path.
    '''

    ### PRIVATE METHODS ###

    def _collect_segment_lys(self):
        entries = sorted(self.segments.glob('*'))
        names = [_.name for _ in entries]
        sources, targets = [], []
        for name in names:
            directory = self.segments / name
            if not directory.is_dir():
                continue
            source = directory / 'illustration.ly'
            if not source.is_file():
                continue
            name = name.replace('_', '-') + '.ly'
            target = self._segments / name
            sources.append(source)
            targets.append(target)
        if not self.builds.is_dir():
            self.builds.mkdir()
        return zip(sources, targets)

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
        command = 'git rev-parse --show-toplevel'
        with abjad.TemporaryDirectoryChange(directory=self):
            lines = abjad.IOManager.run_command(command)
            first_line = lines[0]
            return type(self)(first_line)

    def _get_title_metadatum(self, year=True):
        if year and self.get_metadatum('year'):
            title = self._get_title_metadatum(year=False)
            year = self.get_metadatum('year')
            result = f'{title} ({year})'
            return result
        else:
            result = self.get_metadatum('title')
            result = result or '(untitled score)'
            return result

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

    def _is_in_git_repository(self):
        if not self.exists():
            return False
        path = self.wrapper
        for path_ in path.glob('*'):
            if path_.name == '.git':
                return True
        return False

    def _make_package(self):
        assert not self.exists()
        self.mkdir()
        required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )
        for required_file in required_files:
            boilerplate = type(self)(abjad_configuration.boilerplate_directory)
            if required_file == '__init__.py':
                source = boilerplate / 'empty.py'
            elif required_file == '__metadata__.py':
                source = boilerplate / '__metadata__.py'
            elif required_file == 'definition.py':
                source = boilerplate / 'definition.py'
            else:
                raise ValueError(required_file)
            target = self / required_file
            shutil.copyfile(str(source), str(target))
        paths = self.parent.list_ordered_paths()
        if self not in paths:
            self.parent.add_metadatum('view', None)

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

    def _write_metadata_py(self, metadata):
        import abjad
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
        metadata_lines = f'metadata = {metadata_lines}'
        text = text + '\n' + metadata_lines + '\n'
        metadata_py_path.write_text(text)

    ### PUBLIC METHODS ###

    def copy_boilerplate(self, source_name, target_name=None, values=None):
        r'''Copies `source_name` from boilerplate directory to `target_name` in
        this directory.

        Replaces `values` in target.

        Returns none.
        '''
        assert self.is_dir(), repr(self)
        values = values or {}
        boilerplate = type(self)(abjad_configuration.boilerplate_directory)
        source = boilerplate / source_name
        target_name = target_name or source_name
        target = self / target_name
        shutil.copyfile(str(source), str(target))
        template = target.read_text()
        template = template.format(**values)
        target.write_text(template)

    def get_menu_header(self):
        r'''Gets menu header.

        Returns string.
        '''
        if self.is_scores():
            return 'Abjad IDE - scores directory'
        if not self.is_package_path():
            header = f'Abjad IDE - {directory}'
            return header
        header_parts = []
        score_part = self.contents._get_title_metadatum()
        header_parts.append(score_part)
        if self.is_wrapper():
            header_parts.append('wrapper directory')
        path_parts = type(self)(self.trim()).parts
        path_parts = path_parts[1:]
        if not path_parts:
            directory_part, package_part = None, None
        elif self.is_package_path(('contents', 'wrapper')):
            directory_part, package_part = None, None
        elif len(path_parts) == 1:
            directory_part, package_part = path_parts[0], None
        elif len(path_parts) == 2:
            directory_part, package_part = path_parts
        else:
            message = f'can not classify {self!r}.'
            raise ValueError(message, path_parts)
        if directory_part:
            directory_part = directory_part + ' directory'
            header_parts.append(directory_part)
        if package_part:
            if package_part == '_segments':
                package_part = 'segments'
            else:
                package_part = package_part.replace('_', ' ')
            package_part = self.get_metadatum('name', package_part)
            header_parts.append(package_part)
        header = ' - '.join(header_parts)
        return header

    def make_menu(self, name=None):
        r'''Makes menu to manage path.
        
        Returns menu.
        '''
        import ide
        menu = ide.Menu(directory=self, name=name)
        entries = []
        for path in self.list_secondary_paths():
            entry = ide.MenuEntry(
                display_string=path.name,
                explicit_return_value=path,
                )
            entries.append(entry)
        if entries:
            entries.sort(key=lambda _: _.display_string)
            menu.make_asset_section(
                menu_entries=entries,
                is_numbered=False,
                name='secondary',
                )
        entries = []
        ppp = self._collect_similar_directories()
        for path in self.list_ordered_paths():
            if not self.is_wrapper():
                entry = ide.MenuEntry(
                    display_string=path.get_identifier(),
                    explicit_return_value=path,
                    )
            else:
                entry = ide.MenuEntry(
                    display_string=path.name,
                    explicit_return_value=path,
                    )
            entries.append(entry)
        if entries:
            menu.make_asset_section(menu_entries=entries)
        return menu
