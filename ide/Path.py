import typing

import abjad


class Path(abjad.Path):
    """
    Path.
    """

    ### CLASS VARIABLES ###

    address_characters = {
        "@": "file",
        "%": "directory",
        "^": "source file",
        "*": "PDF",
        "+": "test file",
    }

    ### PRIVATE METHODS ###

    def _find_doctest_files(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob("**/*.py")):
                if "__pycache__" in str(path):
                    continue
                if not path.is_file():
                    continue
                if path.name.startswith("test"):
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.segments.list_paths():
                files.append(path / "definition.py")
                strings.append(path.get_identifier())
        return files, strings

    def _find_editable_files(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob("**/*")):
                if "__pycache__" in str(path):
                    continue
                if not path.is_file():
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.segments.list_paths():
                files.append(path / "definition.py")
                strings.append(path.get_identifier())
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
            for path in sorted(self.glob("**/*.pdf")):
                if "__pycache__" in str(path):
                    continue
                if not path.is_file():
                    continue
                files.append(path)
                strings.append(path.name)
        else:
            for path in self.segments.list_paths():
                files.append(path / "illustration.pdf")
                strings.append(path.get_identifier())
            for path in self.etc.list_paths():
                if path.suffix == ".pdf":
                    files.append(path)
                    strings.append(path.name)
        return files, strings

    def _find_pytest_files(self, force=False):
        files, strings = [], []
        if force or not self.is_score_package_path():
            for path in sorted(self.glob("**/test*.py")):
                if "__pycache__" in str(path):
                    continue
                if not path.is_file():
                    continue
                files.append(path)
                strings.append(path.name)
        return files, strings

    def _get_added_asset_paths(self):
        paths = []
        git_status_lines = self._get_git_status_lines()
        for line in git_status_lines:
            line = str(line)
            if line.startswith("A"):
                path = line.strip("A")
                path = path.strip()
                root = self.wrapper
                path = root / path
                paths.append(path)
        return paths

    def _get_git_status_lines(self):
        with abjad.TemporaryDirectoryChange(directory=self.wrapper):
            command = f"git status --porcelain {self}"
            return abjad.IOManager.run_command(command)

    def _get_repository_root(self):
        if not self.exists():
            return
        if self.wrapper is None:
            path = self
        else:
            path = self.wrapper
        while str(path) != str(path.parts[0]):
            for path_ in path.iterdir():
                if path_.name == ".git":
                    return type(self)(path)
            path = path.parent

    def _get_unadded_asset_paths(self):
        assert self.is_dir()
        paths = []
        root = self.wrapper
        git_status_lines = self._get_git_status_lines()
        for line in git_status_lines:
            line = str(line)
            if line.startswith("?"):
                path = line.strip("?")
                path = path.strip()
                path = root / path
                paths.append(path)
            elif line.startswith("M"):
                path = line.strip("M")
                path = path.strip()
                path = root / path
                paths.append(path)
        paths = [_ for _ in paths]
        return paths

    def _has_pending_commit(self):
        assert self.is_dir()
        command = f"git status {self}"
        with abjad.TemporaryDirectoryChange(directory=self):
            lines = abjad.IOManager.run_command(command)
        clean_lines = []
        for line in lines:
            line = str(line)
            clean_line = line.strip()
            clean_line = clean_line.replace(str(self), "")
            clean_lines.append(clean_line)
        for line in clean_lines:
            if "Changes not staged for commit:" in line:
                return True
            if "Changes to be committed:" in line:
                return True
            if "Untracked files:" in line:
                return True

    def _is_git_unknown(self):
        if not self.exists():
            return False
        git_status_lines = self._get_git_status_lines()
        git_status_lines = git_status_lines or [""]
        first_line = git_status_lines[0]
        if first_line.startswith("?"):
            return True
        return False

    def _parse_part_identifier(self):
        if self.suffix == ".ly":
            part_identifier = None
            with self.open("r") as pointer:
                for line in pointer.readlines():
                    if line.startswith("% part_identifier = "):
                        line = line.strip("% part_identifier = ")
                        part_identifier = eval(line)
                        return part_identifier
        elif self.name.endswith("layout.py"):
            part_identifier = None
            with self.open("r") as pointer:
                for line in pointer.readlines():
                    if line.startswith("part_identifier = "):
                        line = line.strip("part_identifier = ")
                        part_identifier = eval(line)
                        return part_identifier
        else:
            raise TypeError(self)

    def _unadd_added_assets(self):
        paths = []
        paths.extend(self._get_added_asset_paths())
        paths.extend(self._get_modified_asset_paths())
        commands = []
        for path in paths:
            command = f"git reset -- {path}"
            commands.append(command)
        command = " && ".join(commands)
        with abjad.TemporaryDirectoryChange(directory=path):
            abjad.IOManager.spawn_subprocess(command)

    ### PUBLIC METHODS ###

    def get_eol_measure_numbers(self) -> typing.Optional[typing.List[int]]:
        """
        Gets EOL measure numbers from BOL measure numbers stored in metadata.
        """
        bol_measure_numbers = self.get_metadatum("bol_measure_numbers")
        if bol_measure_numbers is None:
            return None
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        final_measure_number = self.get_metadatum("final_measure_number")
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        return eol_measure_numbers

    def is_prototype(self, prototype) -> bool:
        """
        Is true when path is ``prototype``.
        """
        if prototype is True:
            return True
        if bool(prototype) is False:
            return False
        return self.is_score_package_path(prototype)
