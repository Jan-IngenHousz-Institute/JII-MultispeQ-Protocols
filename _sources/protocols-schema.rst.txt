Syntax
======

.. admonition:: Automatically Generated

   This part of the documentation is automatically generated from the schema file used for validating protocols following the 
   `2020-12 draft <https://json-schema.org/draft/2020-12/schema>`_. For more detailed information on protocols, please refer the documentation by
   `PhotosynQ, Inc. <https://help.photosynq.com>`_


_protocol_set_
--------------

Treating protocols as integrated sets

.. code-block:: python

  ## Code Example
  _protocol_set_: [
    {
      "label": "PAM"
    },
    {
      "label": "ECS"
    }
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Object**
  - *Protocol within the protocol set*

----


adc_show
--------

ADC values are outputted in data_raw instead of the regular output

.. code-block:: python

  ## Code Example
  adc_show: 0
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


autogain
--------

Automatic gain control. Multiple gain functions can be added.

.. code-block:: python

  ## Code Example
  autogain: [
    [
      2,
      1,
      3,
      12,
      50000
    ],
    [
      3,
      8,
      1,
      80,
      50000
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array** (Up to 10 items)

  - **Array** (Exactly 5 items)
  - *Order and type for first 5 items (Required)*

    - **Integer**
    - *Minimum:* 0
    - *Maximum:* 9
    - *Index for storing gain settings*

    - **Integer**
    - *Minimum:* 1
    - *Maximum:* 10
    - *Select pulsed LED to test*

    - **Integer**
    - *Minimum:* 1
    - *Maximum:* 3
    - *Select detector to use*

    - **Number**
    - *Minimum:* 1
    - *Maximum:* 65535
    - *Duration in microseconds*

    - **Number**
    - *Minimum:* 0
    - *Maximum:* 65535
    - *Target Value, recommended: 40000-50000*
  - *Automatic gain control settings*

----


averages
--------

Number of times to average the protocol

.. code-block:: python

  ## Code Example
  averages: 3
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 10000

----


averages_delay
--------------

Delay between protocol averages in ms

.. code-block:: python

  ## Code Example
  averages_delay: 2000
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 999999999999

----


dac_lights
----------

When set to 1, values of 'pulsed_lights_brightness' and 'nonpulsed_lights_brightness' are interpreted as 12-bit values (0 - 4095) controlling the DAC instead of PAR values.

.. code-block:: python

  ## Code Example
  dac_lights: 0
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


detectors
---------

Detectors used in measurement, data returned in data_raw

.. code-block:: python

  ## Code Example
  detectors: [
    [
      3
    ],
    [
      3
    ],
    [
      "@s0"
    ],
    [
      3
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**

    - **String, Number** 
    - *Input must be a number, light_intensity, previous_light_intensity, p_light, or a variable reference (@s0, @p0, @n0:1)*

----


energy_min_wake_time
--------------------

Adjust time between 5V shutdown and wake up time in ms

.. code-block:: python

  ## Code Example
  energy_min_wake_time: 7000
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 1000000

----


energy_save_timeout
-------------------

Adjust Energy Save Timeout in ms

.. code-block:: python

  ## Code Example
  energy_save_timeout: 300000
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 1000000

----


environmental
-------------



.. code-block:: python

  ## Code Example
  environmental: [
    [
      "light_intensity"
    ],
    [
      "temperature_humidity_pressure"
    ],
    [
      "temperature_humidity_pressure2"
    ],
    [
      "contactless_temp"
    ],
    [
      "thickness"
    ],
    [
      "compass_and_angle"
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**
  - *Order and type for first 5 items (Required)*

    - **String**
    - ``Any`` of the following


      - *Values:* light_intensity, previous_light_intensity, temperature_humidity_pressure, temperature_humidity_pressure2, thp, thp2, thickness, thickness_raw, compass_and_angle, contactless_temp

    - **Number**

    - **Number**

    - **Number**

    - **Number**
  - *Environmental measurement configuration*

----


environmental_array
-------------------



.. code-block:: python

  ## Code Example
  environmental_array: [
    [
      1
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**
  - *Order and type for first 1 item (Required)*

    - **Number**

----


indicator
---------

Change the color of the indicator Light (MultispeQ v2) defining the color using the channels Red, Green, Blue. The White channel needs to be defined but is ignored. All channels at 0 will turn the light off.

.. code-block:: python

  ## Code Example #1
  indicator: [
    255,
    0,
    0,
    0
  ]
  
  ## Code Example #2
  indicator: [
    0,
    128,
    128,
    0
  ]
  
  ## Code Example #3
  indicator: [
    0,
    0,
    0,
    0
  ]
  



.. rst-class:: inline-style-none

- **Array** (Exactly 4 items)
- *Order and type for first 4 items (Required)*

  - **Integer**
  - *Minimum:* 0
  - *Maximum:* 255
  - *Red channel*

  - **Integer**
  - *Minimum:* 0
  - *Maximum:* 255
  - *Green channel*

  - **Integer**
  - *Minimum:* 0
  - *Maximum:* 2550
  - *Blue channel*

  - **Integer**
  - *Minimum:* 0
  - *Maximum:* 255
  - *White channel*

----


ir_baseline
-----------



.. code-block:: python

  ## Code Example
  ir_baseline: <input>



.. rst-class:: inline-style-none

----


label
-----

Provide a label to a sub-protocol

.. code-block:: python

  ## Code Example #1
  label: "PAM"
  
  ## Code Example #2
  label: "ECS"
  



.. rst-class:: inline-style-none

- **String**

----


max_hold_time
-------------

Set time (in ms) at which the hold commands timeout, default is 15000

.. code-block:: python

  ## Code Example
  max_hold_time: 15000
  



.. rst-class:: inline-style-none

- **Number**

----


measurements
------------

Number of measurement repeats, which is a set of protocols

.. code-block:: python

  ## Code Example
  measurements: 2
  



.. rst-class:: inline-style-none

- **Number**

----


measurements_delay
------------------

Delay between measurement repeats in ms

.. code-block:: python

  ## Code Example
  measurements_delay: 30
  



.. rst-class:: inline-style-none

- **Number**

----


message
-------

Send message to user between pulse sets.

.. code-block:: python

  ## Code Example #1
  message: [
    [
      "alert",
      "Measurement noisy"
    ]
  ]
  
  ## Code Example #2
  message: [
    [
      "prompt",
      "What is the leaf color"
    ]
  ]
  
  ## Code Example #3
  message: [
    [
      "confirm",
      "Is the leaf clamped?"
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array** (Exactly 2 items)
  - *Order and type for first 2 items (Required)*

    - **String**
    - *Values:* alert, prompt, confirm
    - *Message type*

    - **String**
    - *Message content*

----


nonpulsed_lights
----------------

Select LEDs that are not pulsed during a pulse set

.. code-block:: python

  ## Code Example
  nonpulsed_lights: [
    [
      2,
      2,
      2,
      2
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**

    - **String, Number** 
    - *Input must be a number, light_intensity, previous_light_intensity, p_light, or a variable reference (@s0, @p0, @n0:1)*

----


nonpulsed_lights_brightness
---------------------------

LED brightness in µE * s⁻¹ * m⁻² (PAR) for non pulsed lights

.. code-block:: python

  ## Code Example
  nonpulsed_lights_brightness: [
    [
      100,
      100,
      200,
      300
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**

    - **String, Number** 
    - *Input must be a number, light_intensity, previous_light_intensity, p_light, or a variable reference (@s0, @p0, @n0:1)*

----


number_samples
--------------

Number of samples taken by the ADC (analog to digital converter)

.. code-block:: python

  ## Code Example
  number_samples: 10
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 100

----


open_close_start
----------------



.. code-block:: python

  ## Code Example
  open_close_start: 1
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


par_led_start_on_close
----------------------

Ambient light intensity is measured and matched by selected LED until the clamp is closed

.. code-block:: python

  ## Code Example
  par_led_start_on_close: 2
  



.. rst-class:: inline-style-none

- **Integer**
- *Minimum:* 1
- *Maximum:* 10

----


par_led_start_on_open
---------------------

Ambient light intensity is measured and matched by selected LED when the clamp is opened

.. code-block:: python

  ## Code Example
  par_led_start_on_open: 1
  



.. rst-class:: inline-style-none

- **Integer**
- *Minimum:* 1
- *Maximum:* 10

----


par_led_start_on_open_close
---------------------------

Ambient light intensity is measured and matched by selected LED until the clamp is closed

.. code-block:: python

  ## Code Example
  par_led_start_on_open_close: 2
  



.. rst-class:: inline-style-none

- **Integer**
- *Minimum:* 1
- *Maximum:* 10

----


pre_illumination
----------------

Sample illumination with a single LED at a set duration and light intensity

.. code-block:: python

  ## Code Example #1
  pre_illumination: [
    2,
    200,
    600000
  ]
  
  ## Code Example #2
  pre_illumination: [
    [
      2,
      200,
      600000
    ],
    [
      3,
      400,
      600000
    ]
  ]
  



.. rst-class:: inline-style-none

- Only ``One`` of the following

  - **Array** (Exactly 3 items)
  - *Order and type for first 3 items (Required)*

    - **String, Integer** 
    - *Minimum:* 1
    - *Maximum:* 10
    - *LED for illumination*

    - **String, Number** 
    - *Illumination duration in ms*

    - **String, Number** 
    - *Intensity in in µE * s⁻¹ * m⁻² (PAR)*

  - **Array**

    - **Array** (Exactly 3 items)
    - *Order and type for first 3 items (Required)*

      - **String, Integer** 
      - *Minimum:* 1
      - *Maximum:* 10
      - *LED for illumination*

      - **String, Number** 
      - *Illumination duration in ms*

      - **String, Number** 
      - *Intensity in in µE * s⁻¹ * m⁻² (PAR)*

----


protocol_repeats
----------------



.. code-block:: python

  ## Code Example
  protocol_repeats: 30
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 1000000

----


protocols
---------



.. code-block:: python

  ## Code Example
  protocols: 2
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 100

----


protocols_delay
---------------



.. code-block:: python

  ## Code Example
  protocols_delay: 2000
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 999999999

----


pulse_distance
--------------



.. code-block:: python

  ## Code Example
  pulse_distance: <input>



.. rst-class:: inline-style-none

- **Array**

  - **String, Number** 


**Dependencies:** `pulses`_, `pulse_length`_

----


pulse_length
------------



.. code-block:: python

  ## Code Example
  pulse_length: [
    [
      20,
      20,
      20,
      20
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**

    - **String, Number** 


**Dependencies:** `pulses`_, `pulse_distance`_

----


pulsed_lights
-------------



.. code-block:: python

  ## Code Example
  pulsed_lights: [
    [
      1,
      1,
      1,
      2
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**

    - **String, Number** 
    - *Input must be a number, light_intensity, previous_light_intensity, p_light, or a variable reference (@s0, @p0, @n0:1)*


**Dependencies:** `pulsed_lights_brightness`_

----


pulsed_lights_brightness
------------------------



.. code-block:: python

  ## Code Example
  pulsed_lights_brightness: [
    [
      100,
      "auto_bright[1]",
      300,
      100
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array**

    - **String, Number** 


**Dependencies:** `pulsed_lights`_

----


pulses
------

Pulses defines sequence the measurement pulses by the LEDs during a measurement

.. code-block:: python

  ## Code Example
  pulses: [
    10,
    10,
    50,
    "@n1:2",
    100
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Integer, String** 


**Dependencies:** `pulse_length`_, `pulse_distance`_

----


recall
------

Load value from device memory (EEPROM).

.. code-block:: python

  ## Code Example
  recall: [
    "userdef[1]"
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **String**

----


reference
---------

Specify another detector to be measured and subtracted from detector.

.. code-block:: python

  ## Code Example #1
  reference: [
    [
      1
    ]
  ]
  
  ## Code Example #2
  reference: [
    [
      1,
      2
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array** (Exactly 1 item)
  - *Order and type for first 1 item (Required)*

    - **Number**
    - *Minimum:* 1
    - *Maximum:* 4

----


save
----

Save value to device memory (EEPROM).

.. code-block:: python

  ## Code Example
  save: [
    [
      1,
      1500
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array**

  - **Array** (Exactly 2 items)
  - *Order and type for first 2 items (Required)*

    - **Number**
    - *Storage Location*

    - **Number**
    - *Value to be stored in selected location*

----


save_trace_time_scale
---------------------

Set to 1 to save time scale for trace as data_raw_time, otherwise set to 0.

.. code-block:: python

  ## Code Example
  save_trace_time_scale: 1
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


set_led_delay
-------------

Set pre-illumination with a selected LED for a specific amount of time. (Multiple LEDs can be used).

.. code-block:: python

  ## Code Example
  set_led_delay: [
    [
      2,
      20000,
      0
    ],
    [
      2,
      20000,
      100
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array** (Between 1 and 10 items)

  - **Array** (Exactly 3 items)
  - *Order and type for first 3 items (Required)*

    - **Integer**
    - *Values:* 1, 10
    - *LED identification number*

    - **Number**
    - *Minimum:* 0
    - *Illumination duration in ms*

    - **Number**
    - *Values:* 0, 2500
    - *Light intensity in µE * s⁻¹ * m⁻² (PAR)*

----


set_light_intensity
-------------------

Set a constant actinic background light intensity.

.. code-block:: python

  ## Code Example
  set_light_intensity: 1500
  



.. rst-class:: inline-style-none

- **Number**
- *Minimum:* 0
- *Maximum:* 2500

----


spad
----

Measure relative Chlorophyll content (SPAD - Special Products Analysis Division)

.. code-block:: python

  ## Code Example #1
  spad: 1
  
  ## Code Example #2
  spad: [
    1
  ]
  



.. rst-class:: inline-style-none

- Only ``One`` of the following

  - **Integer**
  - *Values:* 0, 1

  - **Array** (Exactly 1 item)
  - *Order and type for first 1 item (Required)*

    - **Integer**
    - *Values:* 0, 1

----


start_on_close
--------------

Set to 1, to wait for the protocol to run until clamp is closed, otherwise set to 0

.. code-block:: python

  ## Code Example
  start_on_close: 1
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


start_on_open
-------------

Set to 1, to wait for the protocol to run until clamp is opened, otherwise set to 0

.. code-block:: python

  ## Code Example
  start_on_open: 1
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


start_on_open_close
-------------------



.. code-block:: python

  ## Code Example
  start_on_open_close: 1
  



.. rst-class:: inline-style-none

- **Integer**
- *Values:* 0, 1

----


v_arrays
--------

Storing variables in arrays available within the protocol

.. code-block:: python

  ## Code Example
  v_arrays: [
    [
      1,
      2
    ],
    [
      100,
      200
    ]
  ]
  



.. rst-class:: inline-style-none

- **Array** (Up to 4 items)

  - **Array** (Up to 10 items)

    - **String, Number** 
    - *Input must be a number, light_intensity, previous_light_intensity, p_light, or a variable reference (@s0, @p0, @n0:1)*

Definitions
-----------

**Array**
  In Python, "array" is analogous to the ``list`` or ``tuple`` type, depending on usage.

**Boolean**
  In Python, "boolean" is analogous to ``bool``. Note that in JSON, ``true`` and ``false`` are lower case, whereas in Python they are capitalized (``True`` and ``False``).

**Integer**
  In Python, "integer" is analogous to the ``int`` type.

**Dependencies**
   When a command has dependencies, all dependent commands have to be used as well for a valid protocol and to ensure proper function.

**Null**
  In Python, ``null`` is analogous to ``None``.

**Number**
  The ``number`` type is used for any numeric type, either ``integers`` or ``floating point`` numbers.

**Object**
  In Python, "objects" are analogous to the ``dict`` type. An important difference, however, is that while Python dictionaries may use anything hashable as a key, in JSON all the keys must be strings.

**String**
  The ``string`` type is used for strings of text. It may contain Unicode characters.
