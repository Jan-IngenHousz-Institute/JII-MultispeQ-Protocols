Elements
========

Basic Protocol
--------------

A basic protocol can used for quick and simple measurements.

.. code-block:: python
   :caption: *Example:* Basic protocol structure

   [
     {
        # Measurement instructions
     }
   ]

Complex Protocol (Sets)
-----------------------

A complex protocol can measure different measurement types defined in a set.

.. code-block:: python
   :caption: *Example:* Complex protocol structure

   [
      {
         "v_arrays": [
            # Arrays with variables
            [100,5,10]
         ]
         "_protocol_sets_": [
            {
              # measurement Instructions
              # for the first Part
              "label": "PAM"
            },
            {
              # measurement Instructions
              # for the second Part
              "label": "ECS"
            }
         ]
      }
   ]


Measuring Lights
----------------

Measuring lights are controlled by defining pulses. Three parameters are required in order to work with pulses.
The number of pulses, the distance between them and the length of pulses.

Single Light Source
^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   :caption: *Example:* Controlling a single measurement light source

   {
     "pulses": [
       20, 50, 20              # Sets of pulses
     ],
   "pulse_distance": [
       10000, 10000, 10000     # Distance between pulses
     ],
   "pulse_length": [
       [ 30 ], [ 30 ], [ 30 ]  # Duration of the pulse
     ]
   }

.. plot:: _static/images/plot-pulses-1-light.py

   *Figure:* Measurement Pulses using a single Light Source and the resulting pulse sequence


Multiple Light Sources
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   :caption: *Example:* Controlling two measurement light sources

   {
     "pulses": [
       20, 50, 20
     ],
     "pulse_distance": [
       10000, 10000, 10000
     ],
     "pulse_length": [
       [ 30, 15 ], [ 30, 15 ], [ 30, 15 ]
     ]
   }

.. plot:: _static/images/plot-pulses-n-light.py

   *Figure:* Measurement Pulses using two Light Sources and the resulting pulse sequence


Detectors
---------

The MultispeQ has two detectors arragend opposite of each other. One to measure within the visible light spectrum covered
by a BG-18 filter, the other detects light in the IR spectrum. Each pulse defined in pulses also needs a corresponding
detector.

The signal from the detectors is returned as an array called ``data_raw``.

.. code-block:: python
   :caption: *Example:* Setting up the detectors for measuing lights

   {
     "pulses": [
       20, 50, 20
     ],
     "pulse_distance": [
       10000, 10000, 10000
     ],
     "pulse_length": [
       [ 30 ], [ 30 ], [ 30 ]
     ],
     "detectors": [
       [ 1 ], [ 1 ], [ 1 ]
     ]
   }

If there is more than one detector per pulse set, the ``data_raw`` array needs to be deconvoluted to extract the separate signals.

.. list-table:: Structure of ``data_raw`` array depending on pulse and detector settings
   :widths: 33 33 34
   :header-rows: 1

   * - Pulses pulses
     - Detectors detectors
     - Output data_raw
   * - ``[ 2 ]``
     - ``[ [0] ]``
     - ``[ ]``
   * - ``[ 2 ]``
     - ``[ [1] ]``
     - ``[ 1, 1 ]``
   * - ``[ 2, 1 ]``
     - ``[ [1], [1] ]``
     - ``[ 1, 1, 1 ]``
   * - ``[ 2, 1 ]``
     - ``[ [3], [1] ]``
     - ``[ 3, 3, 1 ]``
   * - ``[ 2 ]``
     - ``[ [1, 3] ]``
     - ``[ 1, 3, 1, 3 ]``
   * - ``[ 2, 1 ]``
     - ``[ [1, 3], 1 ]``
     - ``[ 1, 3, 1, 3, 1 ]``
   * - ``[ 2 ]``
     - ``[ [1, 3, 1] ]``
     - ``[ 1, 3, 1, 1, 3, 1 ]``


Gain Settings
-------------

When taking a measurement, the signal quality depends amongst other factors on the brightness of the measuring light as well as the duration
of the measuring pulse. Instead of making these settings manually, the autogain function can be used to automatically determine the ideal settings.

.. code-block:: python
   :caption: *Example:* Using auto-gain settings in a protocol to determine pulse duration and brightness

   {
      # Defining the autogain settings
      "autogain": [
        # index, led, detector, pulse length, target intensity
        [ 1, 3, 1, 30, 3000 ]
      ],
      # using the auto_duration<index> for the pulse length
      "pulse_length": [
        [ "auto_duration1" ]
      ],
      "pulsed_lights": [
        [ 3 ]
      ],
      # using the auto_bright<index> for the measuring light brightness
      "pulsed_lights_brightness": [
        [ "auto_bright1" ]
      ],
      # using the detector, already used in the autogain
      "detectors": [
        [ 1 ]
      ]
   }


Sample Pre-Illumination
-----------------------

The pre-illumination allows to adapt a sample to a set light intensity before starting the actual measurement.

.. code-block:: python
   :caption: *Example:* Pre-Illumination of a sample using one or two LEDs

   ## Single LED
   "pre_illumination": [ 2, 200, 60000 ] # LED 2, 200 uE, 1 min
 
   ## Combination of LEDs
   "pre_illumination": [ 
     [2, 200, 60000], # LED 2, 200 uE, 1 min
     [4, 300, 60000]  # LED 4, 300 uE, 1 min
   ]

Environmental Sensors
---------------------

The MultispeQ device has several sensors enabling it to record environmental parameters. Here is an overview of what
information is returned by the available commands.

.. code-block:: python
   :caption: *Example:* Adding environmental sensors to a protocol

   "environmentals": [
      [ "light_intensity" ],
      [ "temperature_humidity_pressure" ],
      [ "contactless_temp" ]
   ]

.. list-table:: Environmental Sensors and the returned data
   :widths: 50 50
   :header-rows: 1

   * - Command
     - Returned 
   * - ``light_intensity``
     - Light intensity in µmol photons × s⁻¹ × m⁻² (PAR)
   * - ``previous_light_intensity``
     - Light intensity from previous measurement (only in _protocols_set_)
   * - ``temperature_humidity_pressure``, ``thp``
     - Temperature (℃), rel. humidity (%), barometric pressure (mbar) - (sensor #1)
   * - ``temperature_humidity_pressure2``, ``thp2``
     - Temperature (℃), rel. humidity (%), barometric pressure (mbar) - (sensor #2)
   * - ``contactless_temp``
     - Contactless Temperature (℃)
   * - ``thickness``
     - Thickness (µm - microns)
   * - ``thickness_raw``
     - Thickness (raw values)
   * - ``compass_and_angle``
     - Roll, pitch, angle and cardinal direction or the Instrument


Ambient Light Intensity (PAR)
-----------------------------

Using the ``light_intensity`` command in a protocol, allows the measured ambient light intensity to be used by the protocol to replicate
the light by the

.. code-block:: python
   :caption: *Example:* Using the ambient light intensity to control an LED

   "_protocol_set_": [
     {
       "environmental": [
         [ "light_intensity" ]
       ],
       "nonpulsed_lights": [
         [ 2 ], [ 2 ]
       ],
       "nonpulsed_lights_brightness": [
         ## Use the ambient light intensity measured by the PAR sensor
         [ "light_intensity" ], [ "light_intensity" ]
       ]
     },
     {
       "nonpulsed_lights": [
         [ 2 ], [ 2 ]
       ],
       "nonpulsed_lights_brightness": [
         ## Use the ambient light intensity from the previous protocol
         [ "previous_light_intensity" ], [ "previous_light_intensity" ]
       ]
     }
     },
     {
       "set_light_intensity": 500,
       "nonpulsed_lights": [
         [ 2 ], [ 2 ]
       ],
       "nonpulsed_lights_brightness": [
         ## Use a set light intensity
         [ "light_intensity" ], [ "light_intensity" ]
       ]
     }
   ]


Repeats
-------

Repeats can be a powerful tool when writing protocols. They allow you to define instructions once and then repeat them, reducing 
complexity and making the protocol easier to write.

Repeats can be especially useful when combined with protocol sets, as they can help minimize the size of the overall protocol.

.. code-block:: python
   :caption: *Example:** How to use different types of repeats in a protocol, including variables

    ## Using fixed repeat values
    [
      {
        # Repeat the entire set
        "set_repeats": 2,
        "_protocol_set_": [
          {
              "label": "Protocol 1",
              # Repeat this protocol within each set repeat
              "protocol_repeats": 3
          },
          {
              "label": "Protocol 2"
          }
        ]
      }
    ]

    ## Using repeats based on variables
    [
      {
        "v_arrays": [ [ 1, 2 ], [ 1, 2, 3 ] ],
        # Repeat the entire set based on the number of elements in the first v_array
        "set_repeats": "#l0",
        "_protocol_set_": [
          {
              "label": "Protocol 1",
              # Repeat this protocol within each set repeat (second v_array)
              "protocol_repeats": "#l1"
          },
          {
              "label": "Protocol 2"
          }
        ]
      }
    ]


Variables (v_arrays)
--------------------

The ``v_arrays`` can hold up to 4 arrays, each with a maximum of 10 numbers. You can add values to these arrays to use them in your protocol.
The selector for a single value, would look like this ``@n0:1``. To access a value based on a protocol or protocol-set repeat, you can use 
``@p0`` for a protocol repeat or ``@s0`` for a protocol-set repeat.

.. code-block:: python
   :caption: *Example:* Using the variables array to define values that can be accessed inside a protocol

   [
     {
       # The variable array
       "v_arrays": [
         [ 100, 200, 400]    # define values
       ],
       "set_repeats": "#3",   # repeat the whole set n times
       "_protocol_sets_": [
         {
           # Define the lights brightness using a variable @s0
           "non_pulsed_lights_brightness": [ "@s0" ],
 
           # repeat the procol set n time
           "protocol_repeats": 3
         }
       ]
     }
   ]


.. list-table:: Accessing the variable array using different commands
   :widths: 25 25 50
   :header-rows: 1

   * - Variable
     - Example
     - Function
   * - ``@s<array>``
     - ``[ "@s0" ]``
     - Set Repeat: With every protocol set repeat the next position in the array is selected and the value used in the protocol
   * - ``@p<array>``
     - ``[ "@p0" ]``
     - Protocol Repeat: With every protocol repeat the next position in the array is selected and the value used in the protocol
   * - ``@n<array>:<value>``
     - ``[ "@n0:0", "@n0:1" ]``
     - Single Value: A specific value is used in the protocol

.. note:: Timeout
   A timeout can be defined to prevent the protocol wait forever for an input through the leaf clamp. Use ``max_hold_time`` to
   set the wait period before the protocol continues. The default is 15 sec ( 15000 ms ).


Protocol Flow Control
---------------------

When starting a measurement with the MultispeQ it starts right away. This might not be usefull outside of a laboratory setting, so flow controll
helps to wait for user input to start the measurement, using the leaf clamp as the input.

.. code-block:: python
   :caption: *Example:* Using the ``par_led_start_on_close`` to controll the measurement start and LED inside the instrument
   
   [
     {
      ## Without LED control
      "start_on_open_close": 1

      ## Controling a PAR LED
      "par_led_start_on_close": 2
     }
   ]

.. list-table:: Comands to use flow control, either with or without LED control
   :widths: 25 15 60
   :header-rows: 1

   * - Command
     - Input
     - Summary
   * - ``start_on_open``
     - 0,1
     - If set to 1 or higher, it will wait until the clamp is opened, then proceed with the rest of the experiment. If the value is set to zero, the command will be ignored.
   * - ``start_on_close``
     - 0,1
     - If set to 1, will wait until the clamp is closed, then proceed with the rest of the experiment. If set to 0, will be ignored.
   * - ``start_on_open_close``
     - 0,1
     - If set to 1, will wait until the clamp is opened then closed, then proceed with the rest of the experiment. If set to 0, will be ignored.
  
   * - ``par_led_start_on_open``
     - 0-10 (LED)
     - If set to 1 or higher, it will wait until the clamp is opened, then proceed with the rest of the experiment. If set to 0, light intensity is set to 0.
   * - ``par_led_start_on_close``
     - 0-10 (LED)
     - If set to 1, will wait until the clamp is closed, then proceed with the rest of the experiment. If set to 0, light intensity is set to 0.
   * - ``par_led_start_on_open_close``
     - 0-10 (LED)
     - If set to 1, will wait until the clamp is opened then closed, then proceed with the rest of the experiment. If set to 0, light intensity is set to 0.


Indicator Light
---------------

The ``MultispeQ v2`` has an indicator light that can be controlled with a protocol to provide information about measurement progress or the 
device status. The table provides a few example colors, but you can find or generate more on 
`W3School <https://www.w3schools.com/html/html_colors_rgb.asp>`_. The White channel is not used an needs to be set to 0.

.. role:: indicator-red
.. role:: indicator-green
.. role:: indicator-blue
.. role:: indicator-yellow
.. role:: indicator-cyan
.. role:: indicator-magenta
.. role:: indicator-black

.. list-table:: Indicator Light Example Colors
   :widths: 50 50
   :header-rows: 1

   * - Name
     - Red, Green, Blue, White
   * - ◉ White
     - ``[255, 255, 255, 0]``
   * - :indicator-red:`◉` Red
     - ``[255, 0, 0, 0]``
   * - :indicator-green:`◉` Green
     - ``[0, 255, 0, 0]``
   * - :indicator-blue:`◉` Blue
     - ``[0, 0, 255, 0]``
   * - :indicator-yellow:`◉` Yellow
     - ``[255, 255, 0, 0]``
   * - :indicator-cyan:`◉` Cyan
     - ``[0, 255, 255, 0]``
   * - :indicator-magenta:`◉` Magenta
     - ``[255, 0, 255, 0]``
   * - :indicator-black:`◉` Turn Light Off
     - ``[0, 0, 0, 0]``
