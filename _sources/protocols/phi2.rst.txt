
.. automodule:: jii_multispeq_protocols.protocols.phi2
  :members:
  :undoc-members:
  :show-inheritance:
  :no-index:

.. rubric:: Import

.. code-block:: python
  :caption: *Example:* Import ``phi2`` into a script

  import jii_multispeq_protocols.phi2 as _phi2

.. rubric:: Protocol

.. code-block:: python

   [{'detectors': [[1], [1], [1]],
  'environmental': [['light_intensity']],
  'nonpulsed_lights': [[2], [2], [2]],
  'nonpulsed_lights_brightness': [['light_intensity'],
                                  [4500],
                                  ['light_intensity']],
  'open_close_start': 1,
  'pulse_distance': [10000, 10000, 10000],
  'pulse_length': [[30], [30], [30]],
  'pulsed_lights': [[3], [3], [3]],
  'pulsed_lights_brightness': [[2000], [30], [30]],
  'pulses': [20, 50, 20]}]

.. rubric:: Analysis Function

.. autofunction:: jii_multispeq_protocols.protocols.phi2._analyze
  :no-index:

.. code-block:: python
  :caption: Analysis Example (requires ``JII-MultispeQ`` package)

  from jii_multispeq import measurement

  ## Take a measurement using the MultispeQ
  data, crc32 = jii_multispeq.measure(port="<Selected Port>", protocol=_phi2, filename=None, notes="")

  ## The analyze function of JII-MultispeQ helps to provide the correct format
  output = measurement.analyze( data, _phi2._analzye )

  ## View Analysis output (as table)
  measurement.view( output )


