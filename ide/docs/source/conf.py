# -*- coding: utf-8 -*-
import sphinx_rtd_theme
from sphinx.highlighting import PygmentsBridge
from pygments.formatters.latex import LatexFormatter
from abjad import abjad_configuration


class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r'''formatcom=\footnotesize'''

PygmentsBridge.latex_formatter = CustomLatexFormatter

### CORE ###
add_function_parentheses = True
copyright = u'2008-2015, Trevor Bača & Josiah Wolf Oberholtzer'
exclude_patterns = []
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'abjad.docs.ext.abjadbook',
    ]
master_doc = 'index'
project = u'Abjad IDE'
release = abjad_configuration.get_abjad_version_string()
source_suffix = '.rst'
templates_path = ['_templates']
version = abjad_configuration.get_abjad_version_string()
pygments_style = 'sphinx'
### HTML ###
html_domain_indices = False
html_last_updated_fmt = '%b %d, %Y'
html_show_sourcelink = True
html_static_path = ['_static']
html_theme = "sphinx_rtd_theme"
html_theme_options = {}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_use_index = False
html_use_smartypants = True
### HTML HELP ###
htmlhelp_basename = 'AbjadAbjadIDEdoc'
### LATEX ###
latex_elements = {
    'inputenc': r'\usepackage[utf8x]{inputenc}',
    'utf8extra': '',
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
    \usepackage{upquote}
    \pdfminorversion=5
    \setcounter{tocdepth}{2}
    \definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
    \definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
    ''',
    }
latex_documents = [
    (
        'index',
        'AbjadExperimentalPackages.tex',
        u'Abjad Experimental Packages Documentation',
        u'Trevor Bača & Josiah Wolf Oberholtzer',
        'manual',
        ),
    ]
latex_use_parts = True
latex_domain_indices = False
### MAN ###
man_pages = [
    (
        'index',
        'abjadide',
        u'Abjad Score PackageManager Documentation',
        [u' Trevor Bača & Josiah Wolf Oberholtzer'],
        1,
        )
    ]
### TEXINFO ###
texinfo_documents = [
    (
        'index',
        'AbjadAbjadIDE',
        u'Abjad Score PackageManager Documentation',
        u'Trevor Bača & Josiah Wolf Oberholtzer',
        'AbjadAbjadIDE',
        'One line description of project.',
        'Miscellaneous',
        ),
    ]
### EXTENSIONS ###
abjadbook_ignored_documents = ()
autodoc_member_order = 'groupwise'
graphviz_dot_args = ['-s32']
graphviz_output_format = 'svg'
intersphinx_mapping = {
    'abjad': ('http://abjad.mbrsi.org', None),
    'python': ('http://docs.python.org/2', None),
    }
todo_include_todos = True