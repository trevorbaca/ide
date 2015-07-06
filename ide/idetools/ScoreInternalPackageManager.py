# -*- encoding: utf-8 -*-
import os
from ide.idetools.PackageManager import PackageManager


class ScoreInternalPackageManager(PackageManager):
    r'''Score-internal package manager.

    Abstract class from which ``MaterialPackageManager`` and
    ``SegmentPackageManager`` inherit.

    Implements sibling package navigation functionality.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ScoreInternalPackageManager, self)
        superclass.__init__(path=path, session=session)
        optional_files = list(self._optional_files)
        optional_files.append('definition.py')
        self._optional_files = tuple(optional_files)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(ScoreInternalPackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'dc': self.check_definition_py,
            'de': self.edit_definition_py,
            'ds': self.write_stub_definition_py,
            })
        return result

    ### PUBLIC METHODS ###

    def check_definition_py(self, dry_run=False):
        r'''Checks ``definition.py``.

        Display errors generated during interpretation.
        '''
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._definition_py_path)
            return inputs, outputs
        stderr_lines = self._io_manager.check_file(self._definition_py_path)
        if stderr_lines:
            messages = [self._definition_py_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(self._definition_py_path)
            self._io_manager._display(message)

    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._go_to_next_package()

    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._go_to_previous_package()

    def interpret_illustration_ly(self, dry_run=False):
        r'''Interprets ``illustration.ly``.

        Makes ``illustration.pdf``.

        Returns pair. List of STDERR messages from LilyPond together
        with list of candidate messages.
        '''
        inputs, outputs = [], []
        if os.path.isfile(self._illustration_ly_path):
            inputs.append(self._illustration_ly_path)
            outputs.append((self._illustration_pdf_path,))
        if dry_run:
            return inputs, outputs
        if not os.path.isfile(self._illustration_ly_path):
            message = 'The file {} does not exist.'
            message = message.format(self._illustration_ly_path)
            self._io_manager._display(message)
            return [], []
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return [], []
        result = self._io_manager.run_lilypond(self._illustration_ly_path)
        subprocess_messages, candidate_messages = result
        return subprocess_messages, candidate_messages