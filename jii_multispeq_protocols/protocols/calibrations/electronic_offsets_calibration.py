"""
Electronic Offsets Calibration
==============================

new electronic offsets calibration

2230
"""

import numpy as np
from scipy import stats
import warnings
from jii_multispeq.analysis import GetProtocolByLabel

_protocol = [
  {
    "v_arrays": [
      [
        -120,
        -150,
        -180,
        -200,
        -300,
        -400
      ],
      [
        -30,
        -40,
        -60,
        -100,
        -120
      ]
    ],
    "set_repeats": 1,
    "_protocol_set_": [
      {
        "label": "test"
      },
      {
        "label": "test",
        "alert": "Clamp panel #1 (white) of the Chlorophyll calibration cards",
        "set_detector_offsets": [
          [
            1,
            0
          ],
          [
            3,
            0
          ]
        ],
        "bleed_correction": 0,
        "do_once": 1
      },
      {
        "autogain": [
          [
            1,
            6,
            1,
            10,
            10000
          ],
          [
            2,
            6,
            1,
            20,
            20000
          ],
          [
            3,
            6,
            1,
            20,
            30000
          ],
          [
            4,
            6,
            1,
            40,
            40000
          ],
          [
            5,
            1,
            3,
            40,
            5000
          ],
          [
            6,
            1,
            3,
            40,
            10000
          ],
          [
            7,
            1,
            3,
            40,
            15000
          ],
          [
            8,
            1,
            3,
            40,
            20000
          ]
        ]
      },
      {
        "label": "card_1",
        "pulses": [
          10,
          10,
          10,
          10
        ],
        "nonpulsed_lights": [
          [
            2
          ],
          [
            2
          ],
          [
            2
          ],
          [
            2
          ]
        ],
        "pulse_distance": [
          4000,
          4000,
          4000,
          4000
        ],
        "nonpulsed_lights_brightness": [
          [
            0
          ],
          [
            0
          ],
          [
            0
          ],
          [
            0
          ]
        ],
        "pulsed_lights": [
          [
            6,
            1
          ],
          [
            6,
            1
          ],
          [
            6,
            1
          ],
          [
            6,
            1
          ]
        ],
        "detectors": [
          [
            1,
            3
          ],
          [
            1,
            3
          ],
          [
            1,
            3
          ],
          [
            1,
            3
          ]
        ],
        "pulsed_lights_brightness": [
          [
            "a_b1",
            "a_b5"
          ],
          [
            "a_b2",
            "a_b6"
          ],
          [
            "a_b3",
            "a_b7"
          ],
          [
            "a_b4",
            "a_b8"
          ]
        ],
        "pulse_length": [
          [
            "a_d1",
            "a_d5"
          ],
          [
            "a_d2",
            "a_d6"
          ],
          [
            "a_d3",
            "a_d7"
          ],
          [
            "a_d4",
            "a_d8"
          ]
        ],
        "protocol_averages": 1,
        "protocol_repeats": 1
      },
      {
        "label": "test",
        "alert": "Clamp panel #9 (white) of the Chlorophyll calibration cards"
      },
      {
        "label": "card_9",
        "pulses": [
          10,
          10,
          10,
          10
        ],
        "nonpulsed_lights": [
          [
            2
          ],
          [
            2
          ],
          [
            2
          ],
          [
            2
          ]
        ],
        "pulse_distance": [
          4000,
          4000,
          4000,
          4000
        ],
        "nonpulsed_lights_brightness": [
          [
            0
          ],
          [
            0
          ],
          [
            0
          ],
          [
            0
          ]
        ],
        "pulsed_lights": [
          [
            6,
            1
          ],
          [
            6,
            1
          ],
          [
            6,
            1
          ],
          [
            6,
            1
          ]
        ],
        "detectors": [
          [
            1,
            3
          ],
          [
            1,
            3
          ],
          [
            1,
            3
          ],
          [
            1,
            3
          ]
        ],
        "pulsed_lights_brightness": [
          [
            "a_b1",
            "a_b5"
          ],
          [
            "a_b2",
            "a_b6"
          ],
          [
            "a_b3",
            "a_b7"
          ],
          [
            "a_b4",
            "a_b8"
          ]
        ],
        "pulse_length": [
          [
            "a_d1",
            "a_d5"
          ],
          [
            "a_d2",
            "a_d6"
          ],
          [
            "a_d3",
            "a_d7"
          ],
          [
            "a_d4",
            "a_d8"
          ]
        ],
        "protocol_averages": 1,
        "protocol_repeats": 1
      },
      {
        "label": "test",
        "alert": "Clamp panel #1 (white) and #9 (white) of BOTH Chlorophyll calibration cards"
      },
      {
        "label": "cards_1_9",
        "pulses": [
          10,
          10,
          10,
          10
        ],
        "nonpulsed_lights": [
          [
            2
          ],
          [
            2
          ],
          [
            2
          ],
          [
            2
          ]
        ],
        "pulse_distance": [
          4000,
          4000,
          4000,
          4000
        ],
        "nonpulsed_lights_brightness": [
          [
            0
          ],
          [
            0
          ],
          [
            0
          ],
          [
            0
          ]
        ],
        "pulsed_lights": [
          [
            6,
            1
          ],
          [
            6,
            1
          ],
          [
            6,
            1
          ],
          [
            6,
            1
          ]
        ],
        "detectors": [
          [
            1,
            3
          ],
          [
            1,
            3
          ],
          [
            1,
            3
          ],
          [
            1,
            3
          ]
        ],
        "pulsed_lights_brightness": [
          [
            "a_b1",
            "a_b5"
          ],
          [
            "a_b2",
            "a_b6"
          ],
          [
            "a_b3",
            "a_b7"
          ],
          [
            "a_b4",
            "a_b8"
          ]
        ],
        "pulse_length": [
          [
            "a_d1",
            "a_d5"
          ],
          [
            "a_d2",
            "a_d6"
          ],
          [
            "a_d3",
            "a_d7"
          ],
          [
            "a_d4",
            "a_d8"
          ]
        ],
        "protocol_averages": 1,
        "protocol_repeats": 1
      }
    ]
  }
]

def _analyze( _data ):
  """
  * Macro for data evaluation on PhotosynQ.org
  * by: David M. Kramer
  * created: May 31, 2020 9:31 AM
  
  This protocol tests for offsets in detectors 1 and 3 by
  comparing measured transmission values usingtaken with the
  same settings, but with three different transmission card 
  setups. Plotting these against the first should give a series
  of lines that intersect at the data offset point.

  The protocol sends the offset values back to the toDevice
  to be used in subtracting off offsets.
  """
  print_vals = 2

  ## Define the output object here
  output = {}

  ## Check if the key time exists in json
  if "time" in _data:
    ## Add key time and value to output
    output["time"] = _data["time"]

  card_1 = GetProtocolByLabel("card_1", _data, True)
  card_1_data = card_1[0]["data_raw"]
  card_1_data_det_1 = card_1_data[0::2]
  card_1_data_det_3 = card_1_data[1::2]

  output["card_1_data_det_3"] = card_1_data_det_3

  if print_vals > 0:
    output["det3"] = "[%s" % repr(card_1_data_det_3)


  card_9 = GetProtocolByLabel("card_9", _data, True)
  card_9_data = card_9[0]["data_raw"]
  card_9_data_det_1 = card_9_data[0::2]
  card_9_data_det_3 = card_9_data[1::2]

  if print_vals > 0:
    output["det3"] += ", %s" % repr(card_9_data_det_3)

  cards_1_9 = GetProtocolByLabel("cards_1_9", _data, True)
  cards_1_9_data = cards_1_9[0]["data_raw"]
  cards_1_9_data_det_1 = cards_1_9_data[0::2]
  cards_1_9_data_det_3 = cards_1_9_data[1::2]

  if print_vals > 0:
    output["det3"] += ", %s]" % repr(cards_1_9_data_det_3)


  ## detector 1 
  ## card 1 v card 9
  output["card_1_data_det_1"] = card_1_data_det_1
  output["card_9_data_det_1"] = card_9_data_det_1

  slope, intercept, r_value, p_value, std_err = stats.linregress(card_1_data_det_1, card_9_data_det_1)

  slope_det_1_1_v_9 = slope
  y_int_det_1_1_v_9 = intercept
  r2_det_1_1_v_9 = r_value**2

  output["r2_det_1_1_v_9"] = np.round(r2_det_1_1_v_9, 7)

  ## card 1 v cards 1+9

  slope, intercept, r_value, p_value, std_err = stats.linregress(card_1_data_det_1, cards_1_9_data_det_1)

  slope_det_1_1_v_1_9 = slope
  y_int_det_1_1_v_1_9 = intercept
  r2_det_1_1_v_1_9 = r_value**2

  output["r2_det_1_1_v_1_9"] = np.round(r2_det_1_1_v_1_9,7)

  ## now calculate the intersection point between the two lines

  ## y1 = m1*x + b1
  ## y2 = m2*x + b2

  ## There should be an intersection point where y1=y2
  ## at which point x should be our offset.
  ## m1*x - m2*x + b1 - b2 = 0
  ## x (m1-m2) = b2 - b1
  ## x = (b2-b1)/(m1-m2)

  offset_det_1 = (y_int_det_1_1_v_1_9 - y_int_det_1_1_v_9)/(slope_det_1_1_v_9-slope_det_1_1_v_1_9)

  output["offset_det_1"] = np.round(offset_det_1,0)

  ## now do the same for detector 3

  slope, intercept, r_value, p_value, std_err = stats.linregress(card_1_data_det_3, card_9_data_det_3)
  slope_det_3_1_v_9 = slope
  y_int_det_3_1_v_9 = intercept
  r2_det_3_1_v_9 = r_value**2

  output["r2_det_3_1_v_9"] = np.round(r2_det_3_1_v_9,7)

  slope, intercept, r_value, p_value, std_err = stats.linregress(card_1_data_det_3, cards_1_9_data_det_3)

  slope_det_3_1_v_1_9 = slope
  y_int_det_3_1_v_1_9 = intercept
  r2_det_3_1_v_1_9 = r_value**2

  output["r2_det_3_1_v_1_9"] = np.round(r2_det_3_1_v_1_9,7)

  offset_det_3 = (y_int_det_3_1_v_1_9 - y_int_det_3_1_v_9)/(slope_det_3_1_v_9-slope_det_3_1_v_1_9)

  output["offset_det_3"] = np.round(offset_det_3,0)

  output["toDevice"] = "set_detector_offset+1+"
  output["toDevice"] += str(np.round(offset_det_1, 0))
  output["toDevice"] += "+"
  output["toDevice"] += "set_detector_offset+3+"
  output["toDevice"] += str(np.round(offset_det_3, 0))
  output["toDevice"] += "+"

  if ((r2_det_1_1_v_9 < 0.99) or (r2_det_1_1_v_1_9 < 0.99) or (r2_det_3_1_v_9 < 0.99 ) or (r2_det_3_1_v_1_9 < 0.99)):
    warnings.warn("Low r² value(s) for the linear regession. This could be caused by the card moving. Repeat the offset calibration.")

  if ((offset_det_1>400) or (offset_det_1 < -300)):
    warnings.warn("High offset value for detector 1 (%s). Consider repeating the offset calibration." % np.round(offset_det_1,1))


  if ((offset_det_3 > 400) or (offset_det_3 < -300)):
    warnings.warn("High offset value for detector 3 (%s). Consider repeating the offset calibration." % np.round(offset_det_3,0))

  ## Return data
  return output


_example = {
  "time": 1600105494848,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "52:00:06:f0",
  "device_battery": 100,
  "device_firmware": 2.3433,
  "sample": [
    [
      {
        "time": 1600105494848,
        "v_arrays": [
          [
            -120,
            -150,
            -180,
            -200,
            -300,
            -400
          ],
          [
            -30,
            -40,
            -60,
            -100,
            -120
          ]
        ],
        "set_repeats": 1,
        "protocol_id": 1,
        "set": [
          {
            "time": 1600105494864,
            "label": "test",
            "data_raw": [

            ]
          },
          {
            "time": 1600105494864,
            "set_detector_offsets": [
              [
                1,
                0
              ],
              [
                3,
                0
              ]
            ],
            "bleed_correction": 0,
            "message": [
              "alert",
              "Clamp panel #1 (white) of the Chlorophyll calibration cards",
              "ok"
            ],
            "label": "test",
            "data_raw": [

            ]
          },
          {
            "time": 1600105499075,
            "autogain": [
              [
                1,
                6,
                1,
                10,
                -4294,
                28
              ],
              [
                2,
                6,
                1,
                20,
                -1342,
                34
              ],
              [
                3,
                6,
                1,
                20,
                -1342,
                35
              ],
              [
                4,
                6,
                1,
                40,
                -1342,
                43
              ],
              [
                5,
                1,
                3,
                40,
                -83,
                4991
              ],
              [
                6,
                1,
                3,
                40,
                -109,
                9069
              ],
              [
                7,
                1,
                3,
                40,
                -143,
                14445
              ],
              [
                8,
                1,
                3,
                40,
                -176,
                19625
              ]
            ],
            "data_raw": [

            ]
          },
          {
            "time": 1600105507127,
            "label": "card_1",
            "data_raw": [
              30,
              4991,
              23,
              4991,
              25,
              4993,
              23,
              4991,
              27,
              4983,
              23,
              4982,
              25,
              4989,
              28,
              4996,
              29,
              5001,
              30,
              4989,
              31,
              9078,
              30,
              9085,
              35,
              9075,
              36,
              9077,
              31,
              9082,
              33,
              9081,
              34,
              9079,
              29,
              9081,
              37,
              9081,
              29,
              9070,
              36,
              14447,
              29,
              14445,
              37,
              14441,
              27,
              14450,
              31,
              14461,
              31,
              14455,
              31,
              14447,
              31,
              14451,
              29,
              14446,
              36,
              14454,
              41,
              19610,
              44,
              19599,
              45,
              19611,
              47,
              19615,
              50,
              19606,
              42,
              19607,
              39,
              19614,
              43,
              19609,
              42,
              19605,
              41,
              19616
            ]
          },
          {
            "time": 1600105507468,
            "message": [
              "alert",
              "Clamp panel #9 (white) of the Chlorophyll calibration cards",
              "ok"
            ],
            "label": "test",
            "data_raw": [

            ]
          },
          {
            "time": 1600105512454,
            "label": "card_9",
            "data_raw": [
              31,
              883,
              25,
              879,
              29,
              883,
              25,
              880,
              28,
              883,
              31,
              877,
              25,
              879,
              26,
              885,
              30,
              880,
              21,
              879,
              31,
              1654,
              30,
              1653,
              32,
              1655,
              31,
              1650,
              31,
              1650,
              33,
              1652,
              34,
              1649,
              33,
              1655,
              35,
              1651,
              30,
              1655,
              35,
              2685,
              35,
              2682,
              31,
              2683,
              34,
              2682,
              29,
              2681,
              29,
              2685,
              31,
              2686,
              29,
              2682,
              31,
              2683,
              31,
              2681,
              47,
              3685,
              44,
              3686,
              43,
              3689,
              42,
              3685,
              46,
              3682,
              42,
              3688,
              46,
              3685,
              43,
              3690,
              45,
              3687,
              41,
              3687
            ]
          },
          {
            "time": 1600105512770,
            "message": [
              "alert",
              "Clamp panel #1 (white) and #9 (white) of BOTH Chlorophyll calibration cards",
              "ok"
            ],
            "label": "test",
            "data_raw": [

            ]
          },
          {
            "time": 1600105519121,
            "label": "cards_1_9",
            "data_raw": [
              26,
              271,
              27,
              274,
              27,
              270,
              27,
              271,
              25,
              275,
              29,
              273,
              26,
              270,
              28,
              275,
              25,
              270,
              25,
              271,
              27,
              539,
              31,
              544,
              32,
              538,
              37,
              541,
              29,
              542,
              31,
              538,
              33,
              539,
              33,
              543,
              31,
              538,
              35,
              539,
              36,
              899,
              31,
              903,
              31,
              905,
              29,
              903,
              35,
              899,
              28,
              898,
              30,
              900,
              29,
              899,
              35,
              902,
              31,
              900,
              47,
              1252,
              45,
              1251,
              41,
              1251,
              45,
              1251,
              47,
              1255,
              43,
              1249,
              46,
              1252,
              47,
              1255,
              43,
              1251,
              43,
              1251
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
  "location": False,
  "time_offset": "America/Detroit"
}