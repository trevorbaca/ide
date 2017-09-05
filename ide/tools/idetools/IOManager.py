import abjad
import io
import pathlib
import platform
import subprocess
from ide.tools.idetools.Configuration import Configuration


class IOManager(abjad.IOManager):
    r'''IO manager.

    ..  container:: example

        ::

            >>> abjad_ide = ide.AbjadIDE(is_test=True)
            >>> io_manager = abjad_ide._io_manager

    '''

    ### CLASS VARAIBLES ###

    __documentation_section__ = 'Classes'

    __slots__ = (
        '_is_example',
        '_is_quitting',
        '_is_redrawing',
        '_is_test',
        '_pending_input',
        '_transcript',
        )

    _editor_extensions = (
        '.ily',
        '.log',
        '.ly',
        '.md',
        '.py',
        '.tex',
        '.txt',
        )

    configuration = Configuration()

    ### INITIALIZER ###

    def __init__(self, is_example=False, is_test=False):
        import ide
        self._is_example = is_example
        self._is_quitting = None
        self._is_redrawing = True
        self._is_test = is_test
        self._pending_input = None
        self._transcript = ide.Transcript()

    ### PRIVATE METHODS ###

    def _clean_up(self):
        if not self._transcript.blocks[-1][-1] == '':
            self._display('')
        self.clear_terminal()

    def _display(self, lines, caps=True, is_menu=False):
        assert isinstance(lines, (str, list)), repr(lines)
        if isinstance(lines, str):
            lines = [lines]
        if caps:
            lines = [abjad.String(_).capitalize_start() for _ in lines]
        if lines:
            self._transcript._append_block(lines, is_menu=is_menu)
        for line in lines:
            print(line)

    def _display_errors(self, lines):
        self._display(lines, caps=False)

    def _get_input(self, message='', split_input=False):
        message = abjad.String(message).capitalize_start() + '> '
        if self._pending_input:
            string = self._pop_from_pending_input()
            print(f'> {string}')
        else:
            # TODO: this can be removed bc all test input should be pending:
            # try block only for pytest
            try:
                string = input(message)
            except OSError:
                string = 'q'
            if string and split_input:
                parts = string.split()
                string = parts[0]
                pending_input = ' '.join(parts[1:])
                if pending_input:
                    self._pending_input = pending_input
        if string == '<return>':
            self._transcript._append_block([message.strip(), ''])
            self._transcript._append_block(['> ', ''])
        else:
            self._transcript._append_block([f'{message}{string}', ''])
            self._transcript._append_block(['> ', ''])
        return abjad.String(string)

    def _invoke_shell(self, statement):
        statement = statement.strip()
        process = subprocess.Popen(
            statement,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        lines = self._read_from_pipe(process.stdout).splitlines()
        lines = lines or []
        lines = [_.strip() for _ in lines]
        self._display(lines, caps=False)

    def _pop_from_pending_input(self):
        parts = self._pending_input.split()
        pending_input = ' '.join(parts[1:])
        self._pending_input = pending_input
        return parts[0].replace('~', ' ')

    ### PUBLIC PROPERTIES ###

    @property
    def transcript(self):
        r'''Gets transcript.

        Returns transcript.
        '''
        return self._transcript

    ### PUBLIC METHODS ###

    def edit(self, path, allow_missing=False, line_number=None):
        r'''Edits file `path`.

        Opens at `line_number` when `line_number` is set.

        Opens at first line when `line_number` is not set.

        Returns none.
        '''
        path = pathlib.Path(path)
        if not allow_missing and not path.is_file():
            message = f'missing {path} ...'
            self._display(message)
            return
        if line_number is None:
            command = f'vim {path}'
        else:
            command = f'vim +{line_number} {path}'
        if self._is_test:
            return
        self.spawn_subprocess(command)

    def interpret_file(self, path):
        r'''Invokes Python or LilyPond on `path`.

        Displays any in-file messaging during interpretation.

        Returns the pair of `stdout_lines` with `stderr_lines`.
        This makes it possible to execute in silent context
        and then display stderr lines after execution.
        '''
        path = pathlib.Path(path)
        if not path.exists():
            message = f'missing {path} ...'
            self._display(message)
            return False
        if path.suffix == '.py':
            command = f'python {path}'
        elif path.suffix == '.ly':
            command = f'lilypond -dno-point-and-click {path}'
        else:
            message = f'can not interpret {path}.'
            raise Exception(message)
        directory = path.parent
        directory = abjad.TemporaryDirectoryChange(directory)
        string_buffer = io.StringIO()
        with directory, string_buffer:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                )
            for line in process.stdout:
                line = line.decode('utf-8')
                print(line, end='')
                string_buffer.write(line)
            process.wait()
            stdout_lines = string_buffer.getvalue().splitlines()
            stderr_lines = self._read_from_pipe(process.stderr)
            stderr_lines = stderr_lines.splitlines()
        exit_code = process.returncode
        return stdout_lines, stderr_lines, exit_code

    def interpret_tex_file(self, tex):
        r'''Interprets TeX file.

        Calls xelatex (or pdflatex) on file TWICE.

        Some LaTeX packages (like tikz) require two passes.

        Returns none.
        '''
        import ide
        if not tex.is_file():
            return
        executables = self.find_executable('xelatex')
        executables = [ide.Path(_) for _ in executables]
        if not executables:
            executable_name = 'pdflatex'
            fancy_executable_name = 'LaTeX'
        else:
            executable_name = 'xelatex'
            fancy_executable_name = 'XeTeX'
        pdf_path = tex.parent / (str(tex.stem) + '.pdf')
        command = f'date > {self.configuration.latex_log_file_path};'
        command += f' {executable_name} -halt-on-error'
        command += f' --jobname={tex.stem}'
        command += f' -output-directory={tex.parent} {tex}'
        command += f' >> {self.configuration.latex_log_file_path} 2>&1'
        command_called_twice = f'{command}; {command}'
        with abjad.TemporaryDirectoryChange(tex.parent):
            self.spawn_subprocess(command_called_twice)
            for path in tex.parent.glob('*.aux'):
                path.unlink()
            for path in tex.parent.glob('*.log'):
                path.unlink()

    def open_file(self, path, line_number=None):
        r'''Opens file `path`.

        Also works when `path` is a list.

        Returns none.
        '''
        line_number_string = ''
        if line_number is not None:
            line_number_string = f' +{line_number}'
        if isinstance(path, str):
            path = pathlib.Path(path)
        if isinstance(path, list):
            path = [pathlib.Path(_) for _ in path]
        if not isinstance(path, list) and not path.is_file():
            pass
        if (isinstance(path, list) and
            all(_.suffix in self._editor_extensions for _ in path)):
            paths = ' '.join([str(_) for _ in path])
            command = f'vim {paths}'
        elif isinstance(path, list):
            paths = path
            paths = ' '.join([str(_) for _ in paths])
            command = f'open {paths}'
        elif (path.name[0] == '.' or path.suffix in self._editor_extensions):
            command = f'vim {path}'
        else:
            command = f'open {path}'
        command = command + line_number_string
        if self._is_test:
            return
        if isinstance(path, list):
            path_suffix = path[0].suffix
        else:
            path_suffix = path.suffix
        if (platform.system() == 'Darwin' and path_suffix == '.pdf'):
            source_path = pathlib.Path(
                self.configuration.boilerplate_directory,
                '__close_preview_pdf__.scr',
                )
            template = source_path.read_text()
            completed_template = template.format(file_path=path)
            script_path = pathlib.Path(
                self.configuration.home_directory,
                '__close_preview_pdf__.scr',
                )
            if script_path.exists():
                script_path.unlink()
            with abjad.FilesystemState(remove=[script_path]):
                script_path.write_text(completed_template)
                permissions_command = f'chmod 755 {script_path}'
                self.spawn_subprocess(permissions_command)
                close_command = str(script_path)
                self.spawn_subprocess(close_command)
        self.spawn_subprocess(command)

    def write(self, path, string):
        r'''Writes `string` to `path`.

        Returns none.
        '''
        path = pathlib.Path(path)
        directory = path.parent
        if not directory.exists():
            directory.mkdir()
        path.write_text(string)
