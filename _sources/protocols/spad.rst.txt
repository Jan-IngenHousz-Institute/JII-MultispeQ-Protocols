
.. automodule:: jii_multispeq_protocols.protocols.spad
  :members:
  :undoc-members:
  :show-inheritance:
  :no-index:

.. rubric:: Import

.. code-block:: python
  :caption: *Example:* Import ``spad`` into a script

  import jii_multispeq_protocols.spad as _spad

.. rubric:: Protocol

.. warning:: Protocol failed automated validation!

  + Path '0 -> _protocol_set_ -> 0 -> spad': [[2, 3, 6], [-1]] is not valid under any of the given schemas

.. code-block:: python

   [{'_protocol_set_': [{'label': 'spad',
                      'protocol_repeats': 1,
                      'spad': [[2, 3, 6], [-1]]}]}]

.. rubric:: Analysis Function

.. autofunction:: jii_multispeq_protocols.protocols.spad._analyze
  :no-index:

.. code-block:: python
  :caption: Analysis Example (requires ``JII-MultispeQ`` package)

  from jii_multispeq import measurement

  ## Take a measurement using the MultispeQ
  data, crc32 = jii_multispeq.measure(port="<Selected Port>", protocol=_spad, filename=None, notes="")

  ## The analyze function of JII-MultispeQ helps to provide the correct format
  output = measurement.analyze( data, _spad._analzye )

  ## View Analysis output (as table)
  measurement.view( output )


