import abjad
import collections
import os
import shutil
from ide.tools.idetools.Configuration import Configuration


class Test(abjad.FilesystemState):
    r'''Test state context manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    _configuration = Configuration()

#    ### INITIALIZER ###
#
#    def __init__(self, keep=None, remove=None):
#        keep = keep or []
#        assert isinstance(keep, collections.Iterable), repr(keep)
#        keep = tuple([str(_) for _ in keep])
#        keep = keep + (str(self._configuration.example_scores_directory),)
#        self._keep = keep
#        remove = remove or []
#        assert isinstance(remove, collections.Iterable), repr(remove)
#        remove = tuple([str(_) for _ in remove])
#        self._remove = remove

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Backs up example scores directory tree.

        Then backs up keep-artifacts.

        Returns none.
        '''
        for path in self.remove:
            assert not os.path.exists(path), repr(path)
        for path in self.keep:
            assert os.path.exists(path), repr(path)
            assert os.path.isfile(path) or os.path.isdir(path), repr(path)
        path = str(self._configuration.example_scores_directory)
        backup_path = path + '.backup'
        shutil.copytree(path, backup_path)
        super(Test, self).__enter__()

    def __exit__(self, exg_type, exc_value, traceback):
        r'''Restores example scores directory tree.

        Returns none.
        '''
        super(Test, self).__exit__(exg_type, exc_value, traceback)
        path = str(self._configuration.example_scores_directory)
        backup_path = path + '.backup'
        assert os.path.exists(backup_path), repr(backup_path)
        if os.path.exists(path):
            shutil.rmtree(path)
        shutil.copytree(backup_path, path)
        shutil.rmtree(backup_path)
