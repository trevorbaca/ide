# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
import sys
if sys.version_info[0] == 2:
    import getters
    import predicates
else:
    from ide.idetools import getters
    from ide.idetools import predicates
del sys


systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'Abjad IDE'