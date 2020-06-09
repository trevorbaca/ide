import abjad


class Path(abjad.Path):
    """
    Path.
    """

    ### CLASS VARIABLES ###

    address_characters = {
        "@": "file",
        "%": "directory",
    }

    ### PRIVATE METHODS ###

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
