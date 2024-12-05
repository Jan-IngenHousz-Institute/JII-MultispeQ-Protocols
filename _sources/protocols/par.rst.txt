
.. automodule:: jii_multispeq_protocols.protocols.par
  :members:
  :undoc-members:
  :show-inheritance:
  :no-index:

.. rubric:: Import

.. code-block:: python
  :caption: *Example:* Import ``par`` into a script

  import jii_multispeq_protocols.par as _par

.. rubric:: Protocol

.. code-block:: python

   [{'averages': 1, 'environmental': [['light_intensity', 0]]}]

.. rubric:: Analysis Function

.. autofunction:: jii_multispeq_protocols.protocols.par._analyze
  :no-index:

.. code-block:: python
  :caption: Analysis Example (requires ``JII-MultispeQ`` package)

  from jii_multispeq import measurement

  ## Take a measurement using the MultispeQ
  data, crc32 = jii_multispeq.measure(port="<Selected Port>", protocol=_par, filename=None, notes="")

  ## The analyze function of JII-MultispeQ helps to provide the correct format
  output = measurement.analyze( data, _par._analzye )

  ## View Analysis output (as table)
  measurement.view( output )


