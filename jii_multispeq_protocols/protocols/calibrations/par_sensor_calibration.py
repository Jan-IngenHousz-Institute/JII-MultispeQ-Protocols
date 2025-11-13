"""
PAR Sensor Calibration
======================

adjusts the MultispeQ PAR sensor values (without changing the color balance) using a known "universal" PAR level and darkness.

When using the CaliQ for calibrating the PAR sensor, make sure it is connected and communicating before starting the calibration procedure.
To check if it is properly connected, go to `Instrument Settings <https://help.photosynq.com/instruments/instrument-settings.html>`_ and test
the connection.

.. warning:: This calibration requires a CaliQ device

ID: 2225
"""

import numpy as np
from jii_multispeq.analysis import GetProtocolByLabel
import warnings

_protocol = [
  {
    "require_firmware": [
      2,
      100.4
    ],
    "_protocol_set_": [
      {
        "check_battery": 1,
        "alert": "Connect the CaliQ USB-C cable to the MultispeQ. Be sure to get the correct orientation."
      },
      {
        "set_par": [
          0.3618,
          -0.2348,
          -0.1362,
          -0.0105,
          6.7386
        ]
      },
      {
        "set_par_dark": 0,
        "par_tweak": 1
      },
      {
        "protocols_pre_delay": 1000,
        "alert": "Clip CaliQ Light Source and CaliQ PAR Sensor together."
      },
      {
        "qlight": [
          1,
          100
        ]
      },
      {
        "qpar": [
          1
        ],
        "label": "pre_qlight_to_qpar",
        "protocol_repeats": 10
      },
      {
        "qpar": [
          1
        ],
        "label": "qlight_to_qpar",
        "protocol_repeats": 10
      },
      {
        "par_tweak": 1,
        "alert": "Place CaliQ Light Source on the MultispeQ PAR sensor. Make sure there is no visible gap. (LED light should be on)"
      },
      {
        "label": "light",
        "environmental": [
          [
            "light_intensity"
          ]
        ],
        "protocol_repeats": 10
      },
      {
        "label": "dark",
        "qlight": [
          1,
          0
        ],
        "environmental": [
          [
            "light_intensity"
          ]
        ],
        "protocol_repeats": 5
      }
    ]
  }
]

def _analyze( _data ):

  """
  * Macro for data evaluation on PhotosynQ.org
  * by: David M. Kramer
  * created: April 3, 2019 2:41 PM
  """

  ## Define the output object here
  output = {}

  ## Check if the key time exists in json
  if "time" in _data:
    ## Add key time and value to output
    output["time"] = _data["time"]

  if ("error" in _data["set"][0]) and _data["set"][0]["error"] == "battery low":
    output["error"] = "Battery level too low for calibration! Please recharge until at least 50%!"
    warnings.warn( output["error"] )
    return output

  q = GetProtocolByLabel("qlight_to_qpar", _data, True)

  qparV = []

  for i in range(len(q)):
    qparV.append( q[i]["qpar"][4])

  output["qparV"] = qparV

  qpar = np.mean(qparV)
  output["qpar"] = qpar

  l = GetProtocolByLabel("light", _data)

  lightV = []
  output["lightV"] = lightV

  for i in range(len(l)):
    lightV.append( l[i]["light_intensity"] )

  light = np.mean(lightV)

  output["measuredPAR_Light"] = light

  d = GetProtocolByLabel("dark", _data)
  dark = d[2]["light_intensity"]

  output["measuredPAR_dark"] = np.round( d[2]["light_intensity"], 3 ) 

  l_d = light - dark
  output["light_minus_dark"] = l_d

  tweak = np.round( qpar / l_d, 3 )

  output["tweak"] = tweak

  if dark > 1:
    warnings.warn("The calibration value for the PAR sensor in the dark is too high (\"%s\"). Repeat the calibration."  % dark)

  if tweak < 0.4 and tweak > 2.1:
    warnings.warn("The PAR tweak value for the PAR sensor is out of range (\"%s\"). Repeat the calibration." % tweak)

  output["toDevice"] = "s+set_par_dark+"
  output["toDevice"] += "%s+" % (-1 * dark)

  output["toDevice"] += "par_tweak+"
  output["toDevice"] += "%s+" % tweak

  output["toDevice"] += "setCalTime+0+setCalOK+0+0+"


  return output

_example = {
  "time": 1564325628718,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "ff:ff:ff:ff",
  "device_battery": 8,
  "device_firmware": 2.21,
  "sample": [
    [
      {
        "time": 1564325628723,
        "protocol_id": 1,
        "set": [
          {
            "time": 1564325628739,
            "error": "battery low"
          }
        ],
        "data_raw": [

        ]
      }
    ]
  ],
  "app_os": "macOS 18.0.0",
  "app_name": "PhotosynQ",
  "app_version": "1.5.2",
  "app_device": "x64",
  "location": False,
  "time_offset": "America/Detroit"
}