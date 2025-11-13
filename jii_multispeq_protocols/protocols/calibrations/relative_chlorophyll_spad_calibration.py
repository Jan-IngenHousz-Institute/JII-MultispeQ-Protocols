"""
Relative Chlorophyll (SPAD) Calibration
=======================================

Follow the instructions prompted by the protocol. Make sure the panels of the calibration cards are properly clamped.

.. warning:: This calibration method requires a set of calibration cards

ID: 1890
"""

import numpy as np
from scipy import stats
from jii_multispeq.analysis import GetProtocolByLabel
import warnings

_protocol = [
  {
    "_protocol_set_": [
      {
        "label": "gain",
        "alert": "Insert SPAD calibration panel 9, and press 'ok' to continue.",
        "auto_blank": [
          [
            2,
            2,
            3,
            100,
            10000
          ],
          [
            6,
            6,
            1,
            100,
            10000
          ],
          [
            3,
            3,
            3,
            100,
            10000
          ]
        ]
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 2 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 3 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 4 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 6 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 7 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 8 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 10 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 11 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      },
      {
        "label": "spad",
        "prompt": "Insert SPAD calibration panel 12 ***AND*** enter the corresponding SPAD value for the panel.",
        "spad": [
          [
            2,
            3,
            6
          ],
          [
            -1
          ]
        ],
        "protocol_repeats": 1
      }
    ]
  }
]

def _analyze( _data ):

  """
  * Macro for data evaluation on PhotosynQ.org
  * by: David M. Kramer
  * created: 2017-06-21 @ 10:36:29
  """

  
  # light_1 = 530 nm top 
  # light_2 = 650 nm top
  # light_3 = 605 nm top 
  # light 4 = blue top 
  # light_5 = 940 nm top 
  
  # light_9 = 940 nm bottom 
  # light_7 =  650 bottom
  # light_8 = 850 nm bottom
  # light 9 = 730 nm bottom
  # light 10 = 880 nm bottom

  ## Define the output object here
  output = {}
  s=[7.8, 16.7, 34.3, 26.5, 39.9, 44, 24, 40, 51]

  output["calibrationValuesStock"] = repr(s)


  ## Check if the key time exists in json
  if "time" in _data:
    ## Add key time and value to output
    output["time"] = _data["time"]

  t = GetProtocolByLabel( "spad", _data, True )
  ab = GetProtocolByLabel( "gain", _data, True )


  for i in range(len(t)):
    if (t[i]["message"][2] != ""):
      s[i] = int(t[i].message[2]) # TODO: check if it is int or float

   
  output["calibrationValues"] = repr(s)

  v655 = []
  v950 = []
  r655 = []
  r950 = []


  for i in range(len(t)): ## cycle through the set of measurements
    v655.append(t[i]["absorbance"][0][0])  ## v is the value of the measurements
    r655.append(t[i]["absorbance"][0][1])  ## r is the reference
    v950.append(t[i]["absorbance"][1][0])  ## v is the value of the measurements
    r950.append(t[i]["absorbance"][1][1])  ## r is the reference

  r2 = []
  maxR2 = 0
  bestOffset = -2000
  spadSlope = 0
  spadYInt = 0

  for offset in np.arange(-200, 200, 10):
    da = []
    
    for i in range(len(t)): ## cycle through the set of measurements
      
      DA655 = np.round(r655[i] - offset) - np.round(v655[i] - offset)
      DA950 = np.round(r950[i]) - np.round(v950[i])
      da.append(DA655 - DA950)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(da, s)

    r2_value = r_value**2

    r2.append(r2_value)
    if r2_value > maxR2:
      maxR2 = r2_value
      bestOffset = offset
      spadSlope = slope
      spadYInt = intercept


  output["bestOffset"] = bestOffset
  output["maxR2"] = np.round(maxR2, 5)
  output["spadSlope"] = np.round(spadSlope, 4)
  output["spadYInt"] = np.round(spadYInt, 4)

  spad=[]

  for i in range(len(t)): ## cycle through the set of measurements
    DA655 = np.log10(r655[i]-bestOffset) - np.log10(v655[i]-bestOffset)
    DA950 = np.log10(r950[i]) - np.log10(v950[i])
    dax = DA655-DA950
    spad.append(np.round(spadYInt + spadSlope*dax, 2))

  output["spad"] = repr(spad)

  output["toDevice"] = ""

  output["toDevice"] += "set_spad_offset+%s+" % np.round(bestOffset, 4)
  output["toDevice"] += "set_spad_scale+%s+" % np.round(spadSlope, 4)
  output["toDevice"] += "set_spad_yint+%s+" % np.round(spadYInt, 4)

  if maxR2 < .97:
    output["test"] = "R2 value low. Calibration card may be out of date"
    warnings.warn( output["test"] )
  else:
    output["test"] = "OK"

  return output

_example = {
  "time": 1553786924729,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "41:00:08:6b",
  "device_battery": 100,
  "device_firmware": 2.011,
  "sample": [
    [
      {
        "time": 1553786924729,
        "protocol_id": 1,
        "set": [
          {
            "time": 1553786924739,
            "message": [
              "prompt",
              "Insert panel 9",
              ""
            ],
            "label": "gain",
            "auto_blank": [
              [
                2,
                2,
                3,
                100,
                -461,
                9286
              ],
              [
                6,
                6,
                1,
                100,
                -303,
                9338
              ],
              [
                3,
                3,
                3,
                100,
                -324,
                9447
              ]
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786933707,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                27992,
                9286,
                -90,
                -0.47641,
                2,
                3,
                655
              ],
              [
                27837,
                9338,
                20,
                -0.474988,
                6,
                1,
                950
              ]
            ],
            "spad": [
              7.863,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786941484,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                14921,
                9286,
                -90,
                -0.204392,
                2,
                3,
                655
              ],
              [
                25923,
                9338,
                20,
                -0.444027,
                6,
                1,
                950
              ]
            ],
            "spad": [
              16.653,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786946755,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                2081,
                9286,
                -90,
                0.635358,
                2,
                3,
                655
              ],
              [
                11169,
                9338,
                20,
                -0.077913,
                6,
                1,
                950
              ]
            ],
            "spad": [
              33.925,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786949693,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                3541,
                9286,
                -90,
                0.411991,
                2,
                3,
                655
              ],
              [
                11675,
                9338,
                20,
                -0.09719,
                6,
                1,
                950
              ]
            ],
            "spad": [
              26.483,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786954833,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                722,
                9286,
                -90,
                1.062462,
                2,
                3,
                655
              ],
              [
                6145,
                9338,
                20,
                0.182217,
                6,
                1,
                950
              ]
            ],
            "spad": [
              40.014,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786958252,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                467,
                9286,
                -90,
                1.226162,
                2,
                3,
                655
              ],
              [
                5311,
                9338,
                20,
                0.245785,
                6,
                1,
                950
              ]
            ],
            "spad": [
              43.666,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786961600,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                3130,
                9286,
                -90,
                0.464162,
                2,
                3,
                655
              ],
              [
                8767,
                9338,
                20,
                0.027464,
                6,
                1,
                950
              ]
            ],
            "spad": [
              23.84,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786969037,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                416,
                9286,
                -90,
                1.267867,
                2,
                3,
                655
              ],
              [
                3779,
                9338,
                20,
                0.39425,
                6,
                1,
                950
              ]
            ],
            "spad": [
              39.773,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1553786972223,
            "message": [
              "prompt",
              "Insert spad sample",
              ""
            ],
            "label": "spad",
            "absorbance": [
              [
                283,
                9286,
                -90,
                1.400309,
                2,
                3,
                655
              ],
              [
                5821,
                9338,
                20,
                0.20582,
                6,
                1,
                950
              ]
            ],
            "spad": [
              51.474,
              36.467,
              -90,
              7.915
            ],
            "data_raw": [

            ]
          }
        ],
        "data_raw": [

        ]
      }
    ]
  ],
  "app_os": "macOS 16.7.0",
  "app_name": "PhotosynQ",
  "app_version": "1.2.1",
  "app_device": "x64",
  "location": False,
  "time_offset": "America/Detroit"
}