Getting Started
===============

This is an introduction on how to create a protocol for a MultispeQ and how they can be saved to a single file
so you can use it with multiple scipts/projects or share it.

.. note:: This is also the standard format if you want to submit your protocol to ``JII-MultispeQ-Protocols``.

.. literalinclude:: _static/examples/template.py
   :language: python
   :linenos:
   :caption: Template for a MultispeQ protocol with an analysis function
   :name: protocol-template

Header
------

The header should contain the protocol name and detailed information about the measurement. You can use 
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ (rst) to format the text inside the header.
This can include list, tables, and other elements supported by the reStructuredText markup language.

.. literalinclude:: _static/examples/template.py
   :language: python
   :lines: 1-7
   :linenos:
   :caption: *Example:* Basic template for a protocol header
   :name: protocol-template-header


Protocol Code
-------------

The default variable name should be ``_protocol``, but any can be used to do the analysis. If needed, the protocol can be generated using a
function, it just needs to be a valid `JSON <https://en.wikipedia.org/wiki/JSON>`_.

.. literalinclude:: _static/examples/template.py
   :language: python
   :lines: 9,10
   :linenos:
   :caption: *Example:* Minimum valid MultispeQ protocol
   :name: protocol-template-code


Analysis Function
-----------------

After the meaurement data is returned by the MultispeQ, it can be analyzed further. For example, the Photosystem II quantum yield needs to be 
derived from a fluorescence trace, since the MultispeQ will not directly return a value. The default function name should be ``_analyze``,
but any can be used to do the analysis.

.. literalinclude:: _static/examples/template.py
   :language: python
   :lines: 12-21
   :linenos:
   :caption: *Example:* Basic function to analyze data
   :name: protocol-template-analyze

.. warning::
   
   When creating an analysis function, keep the calculations and plotting separate. If you would run the function on multiple measurements,
   a potentially large number of plots would be generated, slowing everything down. Instead, take the output of the analysis function and
   then create the graphs to plot the data.

Example Measurement
-------------------

If you want the output returned from the MultispeQ can be saved as an example. The default variable name should be ``_example``,
but any can be used to hold the example.

.. literalinclude:: _static/examples/template.py
   :language: python
   :lines: 23-
   :linenos:
   :caption: *Example:* Measurement returned from MultispeQ
   :name: protocol-template-example

Validation :sup:`beta`
----------------------

This package provides a function to test your protocol to see if there might be an issue. Use the following function to see if
there are any unknown commands used or if there are any other issues.

.. code-block:: python

   # Manual validation (verbose to print errors)
   validate( _protocol, True )

   # In a script
   is_valid, errors = validate( _protocol )

.. automodule:: jii_multispeq_protocols.validate
  :members:
  :undoc-members:
  :show-inheritance:
  :no-index:

Visualization :sup:`beta`
-------------------------

This package provides a function to visualize your protocol as a flow chart using `Mermaid <https://mermaid.js.org/>`_.

.. code-block:: python

   _protocol = [{...}]

   # Generate a chart from a protocol
   chart = generate( _protocol )

   # Generate a chart with reverse direction
   chart = generate( _protocol, direction = 'BT' )

   # Generate a chart with different styles
   chart = generate( _protocol, style = {...} )

.. automodule:: jii_multispeq_protocols.visualize
  :exclude-members:
  :undoc-members:
  :show-inheritance:

.. autofunction:: jii_multispeq_protocols.visualize.generate
   :no-index:

Publish
-------

Of course you can publish your protocol any way you want, but you can also provide it to the JII community, by integrating it
into the ``JII-MultispeQ-Protocols`` package for others to use. To do that, you have to do a pull request for this repository.
Once approved, the version number of the package will be increased and your protocol is now available to the community through
the package.

.. note::
  Find a detailed desciption on how to create protocols on https://help.photosynq.com/protocols/create-edit-protocol.html