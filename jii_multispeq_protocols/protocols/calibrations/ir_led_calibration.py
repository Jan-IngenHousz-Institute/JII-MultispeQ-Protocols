"""
IR LED Calibration
==================

used to adjust the output of non PAR LEDS


.. warning:: These calibration steps require a CaliQ

2229
"""

import numpy as np
import warnings
from jii_multispeq.analysis import GetProtocolByLabel

_protocol = [
  {
    "v_arrays": [
      [
        6,
        8,
        9,
        10,
        5
      ],
      [
        1,
        1,
        1,
        1,
        1
      ],
      [
        -20,
        -50,
        -100,
        -200,
        -400,
        -600,
        -1000,
        -1500,
        -2000,
        -4000
      ],
      [
        2250,
        2250,
        2250,
        2250,
        2250
      ],
      [
        7,
        7,
        7,
        7,
        2
      ]
    ],
    "set_repeats": "#l0",
    "_protocol_set_": [
      {
        "do_once": 1,
        "alert": "Stack panels #1 and #9 and place in clamp",
        "bleed_correction": 0
      },
      {
        "label": "@s0",
        "pulses": [
          1
        ],
        "nonpulsed_lights": [
          [
            1
          ]
        ],
        "pulse_distance": [
          5000
        ],
        "nonpulsed_lights_brightness": [
          [
            -1
          ]
        ],
        "pulsed_lights": [
          [
            "@s0"
          ]
        ],
        "detectors": [
          [
            "@s1"
          ]
        ],
        "pulsed_lights_brightness": [
          [
            "@p2"
          ]
        ],
        "pulse_length": [
          [
            "@s4"
          ]
        ],
        "protocol_repeats": "#l2"
      }
    ]
  }
]


def _analyze( _data ):
  """
   * Macro for data evaluation on PhotosynQ.org
   * by: David M. Kramer
   * created: January 4, 2019 9:02 PM
   * updated: 7/12/24 adjusted saturation error threshhold to 60K from 50K
  """

  ## Define the output object here
  output = {}

  ranges = [0, 150,300,600,1200,3000,6000]
  maxVal = 20000

  ## Check if the key time exists in json
  if "time" in _data:
    ## Add key time and value to output
    output["time"] = _data["time"]

  apparentParSettings = _data["v_arrays"][3]

  settings = _data["v_arrays"][2]
  output["settings"] = repr(settings)
  LEDs = _data["v_arrays"][0]
  output["LEDs"] = repr(LEDs)
  slopes=[]

  optimal = []
  optimalIndex = 0
  saturationError = 0

  output["toDevice"] = ""

  ## Cycle through LEDs
  for i in range(len(LEDs)):
    LED = LEDs[i]
    output["toDevice"] += "par_to_dac_lin+%s+" % LED
    dataSet = GetProtocolByLabel( "%s" % LEDs[i], _data, True )
    numberIntensities = len(dataSet)
    parValues = []
    currentBest = 0
    bestSetting = 0
    for ii in range(numberIntensities):
      if dataSet[ii]["data_raw"][0] > 60000:
        if LED != 5:
          saturationError = 1

      parValues.append(dataSet[ii]["data_raw"][0])

      if (( dataSet[ii]["data_raw"][0] > currentBest ) and ( dataSet[ii]["data_raw"][0] < maxVal )):
        currentBest = dataSet[ii]["data_raw"][0]
        optimalIndex = ii
        bestSetting = settings[ii]

      optimal.append(optimalIndex)

    output["par%s" % LEDs[i]] = repr(parValues)
    slope = -1 * bestSetting / apparentParSettings[i]
    slopes.append(slope)
    for r in range(len(ranges)):
      vv = np.round((slope*ranges[r] + 150),0)
      if vv > 4095:
        vv=4095
      output["toDevice"] += "%s+" % vv

  output["toDevice"] += "par_max_setting+5+4095+"
  output["toDevice"] += "par_max_setting+6+4095+"
  output["toDevice"] += "par_max_setting+8+4095+"
  output["toDevice"] += "par_max_setting+9+4095+"
  output["toDevice"] += "par_max_setting+10+4095+"

  if saturationError > 0:
    warnings.warn("Signal too high, use thicker card.")
  else:
    output["toDevice"] += "setCalTime+3+hello+"

  return output


_example = {
  "time": 1591560748952,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "52:00:12:b7",
  "device_battery": 99,
  "device_firmware": 2.311,
  "sample": [
    [
      {
        "time": 1591560748952,
        "v_arrays": [
          [
            6,
            8,
            9,
            10,
            5
          ],
          [
            1,
            1,
            1,
            1,
            1
          ],
          [
            -20,
            -50,
            -100,
            -200,
            -400,
            -600,
            -1000,
            -1500,
            -2000,
            -4000
          ],
          [
            2250,
            2250,
            2250,
            2250,
            2250
          ],
          [
            7,
            7,
            7,
            7,
            2
          ]
        ],
        "set_repeats": 5,
        "protocol_id": "editor",
        "set": [
          {
            "time": 1591560748952,
            "message": [
              "alert",
              "Insert COLORCAL (SPAD) calibration panel #9 (thick white), hit OK",
              "ok"
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1591560750123,
            "label": "6",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750123,
            "label": "6",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750123,
            "label": "6",
            "data_raw": [
              2
            ]
          },
          {
            "time": 1591560750123,
            "label": "6",
            "data_raw": [
              174
            ]
          },
          {
            "time": 1591560750124,
            "label": "6",
            "data_raw": [
              603
            ]
          },
          {
            "time": 1591560750131,
            "label": "6",
            "data_raw": [
              1030
            ]
          },
          {
            "time": 1591560750137,
            "label": "6",
            "data_raw": [
              1858
            ]
          },
          {
            "time": 1591560750144,
            "label": "6",
            "data_raw": [
              2890
            ]
          },
          {
            "time": 1591560750151,
            "label": "6",
            "data_raw": [
              3895
            ]
          },
          {
            "time": 1591560750157,
            "label": "6",
            "data_raw": [
              7786
            ]
          },
          {
            "time": 1591560750164,
            "s": 1
          },
          {
            "time": 1591560750164,
            "label": "8",
            "data_raw": [
              2451
            ]
          },
          {
            "time": 1591560750171,
            "label": "8",
            "data_raw": [
              2452
            ]
          },
          {
            "time": 1591560750180,
            "label": "8",
            "data_raw": [
              2452
            ]
          },
          {
            "time": 1591560750184,
            "label": "8",
            "data_raw": [
              2649
            ]
          },
          {
            "time": 1591560750191,
            "label": "8",
            "data_raw": [
              3241
            ]
          },
          {
            "time": 1591560750199,
            "label": "8",
            "data_raw": [
              3823
            ]
          },
          {
            "time": 1591560750204,
            "label": "8",
            "data_raw": [
              4980
            ]
          },
          {
            "time": 1591560750211,
            "label": "8",
            "data_raw": [
              6392
            ]
          },
          {
            "time": 1591560750218,
            "label": "8",
            "data_raw": [
              7792
            ]
          },
          {
            "time": 1591560750225,
            "label": "8",
            "data_raw": [
              13240
            ]
          },
          {
            "time": 1591560750232,
            "s": 2
          },
          {
            "time": 1591560750232,
            "label": "9",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750238,
            "label": "9",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750247,
            "label": "9",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750251,
            "label": "9",
            "data_raw": [
              59
            ]
          },
          {
            "time": 1591560750258,
            "label": "9",
            "data_raw": [
              311
            ]
          },
          {
            "time": 1591560750265,
            "label": "9",
            "data_raw": [
              574
            ]
          },
          {
            "time": 1591560750271,
            "label": "9",
            "data_raw": [
              1073
            ]
          },
          {
            "time": 1591560750279,
            "label": "9",
            "data_raw": [
              1695
            ]
          },
          {
            "time": 1591560750284,
            "label": "9",
            "data_raw": [
              2312
            ]
          },
          {
            "time": 1591560750292,
            "label": "9",
            "data_raw": [
              4729
            ]
          },
          {
            "time": 1591560750300,
            "s": 3
          },
          {
            "time": 1591560750300,
            "label": "10",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750305,
            "label": "10",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750313,
            "label": "10",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750318,
            "label": "10",
            "data_raw": [
              1
            ]
          },
          {
            "time": 1591560750325,
            "label": "10",
            "data_raw": [
              702
            ]
          },
          {
            "time": 1591560750332,
            "label": "10",
            "data_raw": [
              1833
            ]
          },
          {
            "time": 1591560750338,
            "label": "10",
            "data_raw": [
              4259
            ]
          },
          {
            "time": 1591560750348,
            "label": "10",
            "data_raw": [
              7386
            ]
          },
          {
            "time": 1591560750351,
            "label": "10",
            "data_raw": [
              10551
            ]
          },
          {
            "time": 1591560750359,
            "label": "10",
            "data_raw": [
              24179
            ]
          },
          {
            "time": 1591560750366,
            "s": 4
          },
          {
            "time": 1591560750366,
            "label": "5",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750372,
            "label": "5",
            "data_raw": [
              0
            ]
          },
          {
            "time": 1591560750381,
            "label": "5",
            "data_raw": [
              406
            ]
          },
          {
            "time": 1591560750385,
            "label": "5",
            "data_raw": [
              3172
            ]
          },
          {
            "time": 1591560750393,
            "label": "5",
            "data_raw": [
              9436
            ]
          },
          {
            "time": 1591560750399,
            "label": "5",
            "data_raw": [
              16037
            ]
          },
          {
            "time": 1591560750405,
            "label": "5",
            "data_raw": [
              29249
            ]
          },
          {
            "time": 1591560750413,
            "label": "5",
            "data_raw": [
              46031
            ]
          },
          {
            "time": 1591560750419,
            "label": "5",
            "data_raw": [
              62851
            ]
          },
          {
            "time": 1591560750426,
            "label": "5",
            "data_raw": [
              62673
            ]
          }
        ],
        "data_raw": [

        ]
      }
    ]
  ],
  "app_os": "macOS 17.7.0",
  "app_name": "PhotosynQ",
  "app_version": "1.8.4",
  "app_device": "x64",
  "location": [
    "42.6912439",
    "-84.4464466"
  ],
  "time_offset": "America/Detroit"
}
