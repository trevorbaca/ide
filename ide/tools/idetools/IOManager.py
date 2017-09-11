import abjad
import io
import subprocess
from ide.tools.idetools.Configuration import Configuration
from ide.tools.idetools.Path import Path
from ide.tools.idetools.Transcript import Transcript


class IOManager(abjad.IOManager):
    r'''IO manager.

    ..  container:: example

        ::

            >>> ide.IOManager()
            IOManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    __slots__ = (
        '_pending_input',
        '_terminal_dimensions',
        '_transcript',
        )

    configuration = Configuration()

    ### INITIALIZER ###

    def __init__(self, terminal_dimensions=None):
        self._pending_input = None
        self._terminal_dimensions = terminal_dimensions
        self._transcript = Transcript()

    ### PUBLIC PROPERTIES ###

    @property
    def terminal_dimensions(self):
        r'''Gets terminal dimensions.

        Returns pair or none.
        '''
        return self._terminal_dimensions

    @property
    def transcript(self):
        r'''Gets transcript.

        Returns transcript.
        '''
        return self._transcript

    ### PUBLIC METHODS ###

    @staticmethod
    def change(directory):
        r'''Makes temporary directory change context manager.
        '''
        return abjad.TemporaryDirectoryChange(directory=directory)

    @staticmethod
    def cleanup(remove=None):
        r'''Makes filesystem state context manager.
        '''
        return abjad.FilesystemState(remove=remove)

    def confirm(self, message='ok?'):
        r'''Confirms.

        Returns true or false.
        '''
        result = self.get(message)
        if isinstance(result, str):
            if result == '':
                return False
            if 'yes'.startswith(result.lower()):
                return True
            if 'no'.startswith(result.lower()):
                return False

    def display(self, lines, is_menu=False, raw=False):
        r'''Displays lines.

        Returns none.
        '''
        assert isinstance(lines, (str, list)), repr(lines)
        if isinstance(lines, str):
            lines = [lines]
        if not raw:
            lines = [abjad.String(_).capitalize_start() for _ in lines]
        if lines:
            self.transcript.append(lines, is_menu=is_menu)
        if self._terminal_dimensions:
            height, width = self._terminal_dimensions
            lines = [_[:width] for _ in lines]
        for line in lines:
            print(line)

    def display_errors(self, lines):
        r'''Displays errors.

        Returns none.
        '''
        self.display(lines, raw=True)

    def get(self, prompt='', split_input=False):
        r'''Gets user input.

        Returns none when user enters lone return.

        Returns string when user types input and then hits return.
        '''
        prompt = prompt or ''
        prompt = abjad.String(prompt).capitalize_start() + '> '
        if self._pending_input:
            parts = self._pending_input.split()
            pending_input = ' '.join(parts[1:])
            self._pending_input = pending_input
            string = parts[0].replace('~', ' ')
            print(f'{prompt}{string}')
        else:
            string = input(prompt)
            if string and split_input and not string.startswith('!'):
                parts = string.split()
                string = parts[0]
                pending_input = ' '.join(parts[1:])
                if pending_input:
                    self._pending_input = pending_input
        if string in ('', '<return>'):
            self.transcript.append([prompt.strip(), ''])
            self.transcript.append(['> ', ''])
            return
        else:
            self.transcript.append([f'{prompt}{string}', ''])
            self.transcript.append(['> ', ''])
            return abjad.String(string)

    def interpret_file(self, path):
        r'''Invokes Python or LilyPond on `path`.

        Displays any in-file messaging during interpretation.

        Returns the pair of `stdout_lines` with `stderr_lines`.
        This makes it possible to execute in silent context
        and then display stderr lines after execution.
        '''
        path = Path(path)
        if not path.exists():
            message = f'missing {path} ...'
            self.display(message)
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
        if not tex.is_file():
            return
        executables = self.find_executable('xelatex')
        executables = [Path(_) for _ in executables]
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

    def invoke_shell(self, statement):
        r'''Invokes shell.

        Returns none.
        '''
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
        self.display(lines, raw=True)

    def pending_input(self, string):
        r'''Sets pending input.

        Returns string.
        '''
        self._pending_input = string

    def write(self, path, string):
        r'''Writes `string` to `path`.

        Returns none.
        '''
        path = Path(path)
        directory = path.parent
        if not directory.exists():
            directory.mkdir()
        path.write_text(string)
