.. _ide--Configuration:

Configuration
=============

.. automodule:: ide.Configuration

.. currentmodule:: ide.Configuration

.. container:: svg-container

   .. inheritance-diagram:: ide
      :lineage: ide.Configuration

.. autoclass:: Configuration

   .. autosummary::
      :nosignatures:

      always_ignore
      editor_suffixes
      noneditor_suffixes

   .. autosummary::
      :nosignatures:

      aliases
      aliases_file_path
      boilerplate_directory
      composer_scores_directory
      configuration_directory
      ide_directory
      latex_log_file_path
      test_scores_directory

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Configuration.__delitem__

   .. container:: inherited

      .. automethod:: Configuration.__format__

   .. container:: inherited

      .. automethod:: Configuration.__getitem__

   .. container:: inherited

      .. automethod:: Configuration.__iter__

   .. container:: inherited

      .. automethod:: Configuration.__len__

   .. container:: inherited

      .. automethod:: Configuration.__repr__

   .. container:: inherited

      .. automethod:: Configuration.__setitem__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Configuration.get

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Configuration.aliases

   .. autoattribute:: Configuration.aliases_file_path

   .. autoattribute:: Configuration.boilerplate_directory

   .. autoattribute:: Configuration.composer_scores_directory

   .. autoattribute:: Configuration.configuration_directory

   .. container:: inherited

      .. autoattribute:: Configuration.configuration_file_path

   .. container:: inherited

      .. autoattribute:: Configuration.home_directory

   .. autoattribute:: Configuration.ide_directory

   .. autoattribute:: Configuration.latex_log_file_path

   .. container:: inherited

      .. autoattribute:: Configuration.temp_directory

   .. autoattribute:: Configuration.test_scores_directory