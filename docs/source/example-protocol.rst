Example Protocol (ϕₗₗ)
======================

We take a Photosystem II (PSII) quantum yield measurement as an example to explain how to create a protocol for the MultispeQ as
well as the function to calculate the parameters from the recorded fluorescence signal.

Fluorescence Trace
------------------

The trace below is an example of what could be recorded by the MultispeQ and which could be used to calculate the PSII quantum
yield based of the parameters Fs and Fm'.

.. plot:: _static/images/plot-phi2.py

   *Figure:* Fluorescence trace recorded to determine the Photosystem II quantum yield.

Measurement Protocol
--------------------

The measurement consists of three sequential phases with a total of 90 measurement pulses at a distance of 10000 µs or 10 ms and
a duration of 30 µs. The weak measuring light (``pulsed_lights``) is provided by the LED 3 at a high light intestity of 2000
(``pulsed_lights_brightness``):

1. Initial Ambient Phase
   - 20 pulses delivered at ambient light intensity (light_intensity)
   - Establishes baseline response

2. Saturation Phase
   - 50 pulses delivered at saturating light intensity (4500)
   - Tests maximum photosynthetic capacity

3. Recovery Phase
   - 20 pulses delivered at ambient light intensity (light_intensity)
   - Measures return to baseline conditions

The ``nonpulsed_lights`` define the actinic light during the measurement using LED 2, as well as the saturating pulse.

During each Phase the ``detector`` 1 (IR) is used. Further, the ``environmental`` sensors are used (light_intensity)
to measure the ambient light intensity in PAR (µmol photons × s⁻¹ × m⁻²).

Lastly, the ``"open_close_start": 1`` command starts the protocol after the leaf clamp is opened and closed
around the leaf.

This measurement structure provides all necessary data points to accurately assess photosystem II efficiency
and its response to varying light conditions as the light intensity is not fixed, but the ambient light
intensity is used.

.. literalinclude:: ../../jii_multispeq_protocols/protocols/phi2.py
   :language: python
   :linenos:
   :lines: 14-45
   :caption: Template for a MultispeQ protocol with an analysis function
   :name: protocol-phi2-1

Calculating Parameters
----------------------

The fluorescence trace recorded is available in ``data_raw``. To calculte the Photosystem II quantum yield (:math:`\Phi_{II}`),
the steady state and maximum fluorescence are needed.

.. math::

    \Phi_{II} = \frac{ Fm' - Fs }{Fm'}

Further, with the ambiennt light intensity, the linear electron flow (LEF) can be calculated.
The absortivity is need as well and in most cases 0.45 is a good estimation.

.. math::

    LEF = \Phi_{II} \times PAR \times 0.45

Since the traces can have noise, five data points are collected and averaged to determine the
Fs and Fm' values. For this the numpy package is used.

.. literalinclude:: ../../jii_multispeq_protocols/protocols/phi2.py
   :language: python
   :linenos:
   :lines: 12-13,47-69
   :caption: Template for a MultispeQ protocol with an analysis function
   :name: protocol-phi2-2

.. code-block:: python
    :caption: Example output of the ``_analysis`` function

    { 
      'Fs': 5817.25,
      'Fmp': 13056.6,
      'Phi2': 0.554,
      'LEF': 3.770,
      'PAR': 17,
      'Fluorescence Trace': [273, 270, 248, 242, 240, 239, 234, 234, 238, 254, ...]
    }
