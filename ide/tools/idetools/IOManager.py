from __future__ import print_function
import abc
import abjad
import codecs
import pathlib
import platform
import subprocess
import sys
import traceback
from ide.tools.idetools.Configuration import Configuration
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


configuration = Configuration()


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
        '_session',
        '_transcript',
        )

    _tab = 4 * ' '

    ### INITIALIZER ###

    def __init__(self, session=None):
        from ide.tools.idetools.Transcript import Transcript
        assert session is not None
        self._session = session
        self._transcript = Transcript()

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of IO manager.

        ..  container:: example

            ::

                >>> io_manager
                IOManager()

        Returns string.
        '''
        return f'{type(self).__name__}()'

    ### PRIVATE METHODS ###

    def _clean_up(self):
        if not self._transcript[-1][-1] == '':
            self._display('')
        self.clear_terminal()
        if self._session.is_test:
            return

    def _confirm(self, message='ok?', include_chevron=False):
        getter = self._make_getter(include_newlines=False)
        getter.append_yes_no_string(message, include_chevron=include_chevron)
        result = getter._run()
        if isinstance(result, str):
            if result == '':
                return False
            if 'yes'.startswith(result.lower()):
                return True
            if 'no'.startswith(result.lower()):
                return False

    def _display(self, lines, caps=True, is_menu=False):
        assert isinstance(lines, (str, list)), repr(lines)
        if isinstance(lines, str):
            lines = [lines]
        if caps:
            lines = [abjad.String(_).capitalize_start() for _ in lines]
        if lines:
            self._transcript._append_entry(lines, is_menu=is_menu)
        for line in lines:
            print(line)

    def _display_errors(self, lines):
        self._display(lines, caps=False)

    @staticmethod
    def _get_greatest_version_number(version_directory):
        version_directory = pathlib.Path(version_directory)
        if not version_directory.is_dir():
            return 0
        greatest_number = 0
        for entry in sorted(version_directory.glob('*')):
            number = 0
            try:
                number = int(entry.stem[-4:])
            except ValueError:
                pass
            if greatest_number < number:
                greatest_number = number
        return greatest_number

    @staticmethod
    def _get_one_line_menu_summary(argument):
        if isinstance(argument, (type, abc.ABCMeta)):
            return argument.__name__
        elif isinstance(argument, str):
            return argument
        else:
            return repr(argument)

    def _handle_input(
        self,
        message,
        include_chevron=True,
        include_newline=False,
        prompt_character='>',
        capitalize_prompt=True,
        ):
        r'''Handles user input.
        Appends user input to command history.
        Appends user input to IO transcript.
        Returns command selected by user.
        '''
        found_default_token = False
        if capitalize_prompt:
            message = abjad.String(message).capitalize_start()
        if include_chevron:
            message = message + prompt_character + ' '
        else:
            message = message + ' '
        if not self._session.pending_input:
            was_pending_input = False
            # try block only for pytest
            try:
                input_ = input(message)
            except OSError:
                input_ = 'q'
            if include_newline:
                if not input_ == 'help':
                    print('')
        else:
            was_pending_input = True
            input_ = self._pop_from_pending_input()
            if input_ == '<return>':
                found_default_token = True
        if found_default_token:
            menu_chunk = [message.strip()]
            if include_newline:
                if not input_ == 'help':
                    menu_chunk.append('')
            self._transcript._append_entry(menu_chunk)
            if was_pending_input:
                for string in menu_chunk:
                    print(string)
            menu_chunk = ['> ']
            if include_newline:
                if not input_ == 'help':
                    menu_chunk.append('')
            self._transcript._append_entry(menu_chunk)
            if was_pending_input:
                for string in menu_chunk:
                    print(string)
        else:
            menu_chunk = []
            menu_chunk.append(f'{message}{input_}')
            if include_newline:
                if not input_ == 'help':
                    menu_chunk.append('')
            self._transcript._append_entry(menu_chunk)
            if was_pending_input:
                for string in menu_chunk:
                    print(string)
        return input_

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

    def _make_getter(
        self,
        allow_none=False,
        include_chevron=True,
        include_newlines=False,
        ):
        import ide
        getter = ide.Getter(
            allow_none=allow_none,
            include_chevron=include_chevron,
            include_newlines=include_newlines,
            io_manager=self,
            )
        return getter

    def _make_interaction(self):
        import ide
        return ide.Interaction(io_manager=self)

    def _make_menu(
        self,
        directory=None,
        header=None,
        name=None,
        subtitle=None,
        ):
        import ide
        return ide.Menu(
            directory=directory,
            header=header,
            name=name,
            subtitle=subtitle,
            )

    def _make_selector(
        self,
        is_ranged=False,
        items=None,
        menu_entries=None,
        menu_header=None,
        target_name=None,
        ):
        import ide
        return ide.Selector(
            is_ranged=is_ranged,
            items=items,
            menu_entries=menu_entries,
            menu_header=menu_header,
            target_name=target_name,
            )

    def _pop_from_pending_input(self):
        if self._session.pending_input is None:
            return None
        elif self._session._pending_input == '':
            self._session._pending_input = None
            return None
        elif self._session.pending_input.startswith('{{'):
            index = self._session.pending_input.find('}}')
            input_ = self._session.pending_input[2:index]
            pending_input = self._session.pending_input[index + 2:]
            pending_input = pending_input.strip()
        else:
            input_parts = self._session.pending_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(input_parts):
                if part == '-' or not part.endswith((',', '-')):
                    break
            first_parts = input_parts[:i + 1]
            rest_parts = input_parts[i + 1:]
            input_ = ' '.join(first_parts)
            pending_input = ' '.join(rest_parts)
        input_ = input_.replace('~', ' ')
        self._session._pending_input = pending_input
        return input_

    @staticmethod
    def _trash_file(file_path):
        file_path = pathlib.Path(file_path)
        if not file_path.is_file():
            return
        file_path.unlink()

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
        if self._session.is_test:
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
        string_buffer = StringIO()
        with directory, string_buffer:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                )
            for line in process.stdout:
                #if sys.version_info[0] == 3:
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
        executables = [ide.PackagePath(_) for _ in executables]
        if not executables:
            executable_name = 'pdflatex'
            fancy_executable_name = 'LaTeX'
        else:
            executable_name = 'xelatex'
            fancy_executable_name = 'XeTeX'
        pdf_path = tex.parent / (str(tex.stem) + '.pdf')
        command = f'date > {configuration.latex_log_file_path};'
        command += f' {executable_name} -halt-on-error'
        command += f' --jobname={tex.stem}'
        command += f' -output-directory={tex.parent} {tex}'
        command += f' >> {configuration.latex_log_file_path} 2>&1'
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
        vim_extensions = (
            '.md',
            '.py',
            '.tex',
            '.txt',
            )
        if not isinstance(path, list) and not path.is_file():
            pass
        if (isinstance(path, list) and
            all(_.suffix in vim_extensions for _ in path)):
            paths = ' '.join([str(_) for _ in path])
            command = f'vim {paths}'
        elif isinstance(path, list):
            paths = path
            paths = ' '.join([str(_) for _ in paths])
            command = f'open {paths}'
        elif (path.name[0] == '.' or
            path.suffix in vim_extensions):
            command = f'vim {path}'
        else:
            command = f'open {path}'
        command = command + line_number_string
        if self._session.is_test:
            return
        if isinstance(path, list):
            path_suffix = path[0].suffix
        else:
            path_suffix = path.suffix
        if (platform.system() == 'Darwin' and path_suffix == '.pdf'):
            source_path = pathlib.Path(
                configuration.boilerplate_directory,
                '__close_preview_pdf__.scr',
                )
            template = source_path.read_text()
            completed_template = template.format(file_path=path)
            script_path = pathlib.Path(
                configuration.home_directory,
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
