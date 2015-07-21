# -*- encoding: utf-8 -*-
from ide.idetools.FileWrangler import FileWrangler


class BuildFileWrangler(FileWrangler):
    r'''Build wrangler.

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> wrangler = ide.idetools.BuildFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            BuildFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(BuildFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'build'
        self._file_wrangler_type = 'build'
        self._score_storehouse_path_infix_parts = ('build',)

    ### PRIVATE METHODS ###

    def _make_build_artifact_menu_section(self, menu):
        commands = []
        commands.append(('back cover - generate latex source', 'bcg'))
        commands.append(('back cover - interpret latex source', 'bci'))
        commands.append(('draft - collect segment files', 'dc'))
        commands.append(('draft - generate latex source', 'dg'))
        commands.append(('draft - interpret latex source', 'di'))
        commands.append(('front cover - generate latex source', 'fcg'))
        commands.append(('front cover - interpret latex source', 'fci'))
        commands.append(('music - collect segment files', 'mc'))
        commands.append(('music - generate lilypond source', 'mg'))
        commands.append(('music - interpret lilypond source', 'mi'))
        commands.append(('preface - generate latex source', 'pg'))
        commands.append(('preface - interpret latex source', 'pi'))
        commands.append(('score - generate latex source', 'sg'))
        commands.append(('score - interpret latex source', 'si'))
        commands.append(('score - push pdf to distribution directory', 'sp'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='build artifacts',
            )

    def _make_main_menu(self):
        superclass = super(BuildFileWrangler, self)
        menu = superclass._make_main_menu()
        if self._session.is_in_score:
            self._make_build_artifact_menu_section(menu)
        return menu