.. _ide--Response:

Response
========

.. automodule:: ide.Response

.. currentmodule:: ide.Response

.. container:: svg-container

   .. inheritance-diagram:: ide
      :lineage: ide.Response

.. autoclass:: Response

   .. autosummary::
      :nosignatures:

      get_path
      is_address
      is_command
      is_path
      is_segment_name
      is_shell

   .. autosummary::
      :nosignatures:

      pair
      pattern
      payload
      prefix
      string

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Response.__format__

   .. container:: inherited

      .. automethod:: Response.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Response.get_path

   .. automethod:: Response.is_address

   .. automethod:: Response.is_command

   .. automethod:: Response.is_path

   .. automethod:: Response.is_segment_name

   .. automethod:: Response.is_shell

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Response.pair

   .. autoattribute:: Response.pattern

   .. autoattribute:: Response.payload

   .. autoattribute:: Response.prefix

   .. autoattribute:: Response.string