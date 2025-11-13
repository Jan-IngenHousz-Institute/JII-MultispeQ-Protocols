"""
Reset to Default Settings
=========================

Reset the MultispeQ to its default settings and remove all calibrations

2221

"""

import warnings

_protocol = [
  {
    "recall": [
      "settings"
    ]
  }
]

def _analyze( _data ):
  """
  * Macro for data evaluation on PhotosynQ.org
  * by: David M. Kramer
  * created: December 24, 2018 6:50 PM
  """
  
  ## Define the output object here
  output = {}

  ## Check if the key time exists in json
  if "time" in _data:
    ## Add key time and value to output
    output["time"] = _data["time"]

  s = _data["recall"]["settings"]

  output["firmware"] = s["firmware"]
  if float(s["firmware"]) < 2.3:
    warnings.warn("Use only on firmware versions > 2.3")
  else:
    output["toDevice"] = ""

    output["toDevice"] += "reset_detector_offsets+"

    for i in range(7):
      output["toDevice"] += "setCalOK+%s+0+" % i

    output["toDevice"] += "set_shutdown_time+1800+hello+"

  return output


_example = {
  "time": 1591302851665,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "52:00:13:24",
  "device_battery": 92,
  "device_firmware": 2.31,
  "sample": [
    [
      {
        "time": 1591302851665,
        "protocol_id": 1,
        "recall": {
          "time": 1591302851672,
          "settings": {
            "time": 1591302851672,
            "device_id": "52:00:13:24",
            "device_version": 2,
            "firmware": 2.31,
            "compiled": [
              "Jun  4 2020",
              "16:29:52"
            ],
            "calOK": [
              0,
              1,
              0,
              1,
              1
            ],
            "calTimes": [
              1591057563,
              -1,
              1591062879,
              -1,
              -1,
              -1,
              -1,
              1591064470
            ],
            "device_mod": 0,
            "mag_address": 15,
            "mag_x_scale": 0,
            "mag_y_scale": 0,
            "mag_z_scale": 0,
            "light_slope_all": [
              0.362
            ],
            "light_slope_r": [
              -0.235
            ],
            "light_slope_g": [
              -0.136
            ],
            "light_slope_b": [
              -0.01
            ],
            "light_yint": [
              -6.719
            ],
            "bleed3": [
              [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ],
              [
                -38,
                120,
                198,
                236,
                293,
                367,
                456,
                547
              ],
              [
                1,
                6,
                1,
                -7,
                -14,
                -34,
                -41,
                -71
              ],
              [
                -3,
                -4,
                5,
                20,
                17,
                86,
                144,
                209
              ],
              [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ],
              [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ],
              [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ],
              [
                -24,
                26,
                0,
                26,
                19,
                38,
                40,
                88
              ],
              [
                1,
                4,
                5,
                9,
                15,
                26,
                44,
                50
              ],
              [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
              ]
            ],
            "thickness_a": 21188.332,
            "thickness_b": -1.055,
            "thickness_c": 13119.174,
            "mag_orientation": 1,
            "open_position": 36280,
            "closed_position": 34792,
            "spad_scale": 46.7,
            "spad_offset": -190,
            "spad_yint": 6.526,
            "blink_mode": 1,
            "pilot_blink": 1,
            "status_blink": 1,
            "shutdown_time (s)": 1800,
            "usb_on": 1,
            "pix_pin": 14,
            "par_method": 3,
            "par_map": [
              [
                49,
                114,
                180,
                320,
                643,
                1429,
                3784
              ],
              [
                69,
                127,
                181,
                287,
                496,
                925,
                2201
              ],
              [
                37,
                249,
                501,
                1172,
                4095,
                4095,
                4095
              ],
              [
                109,
                234,
                363,
                621,
                1181,
                2426,
                4095
              ],
              [
                65535,
                65535,
                65535,
                65535,
                10240,
                17796,
                28672
              ],
              [
                150,
                417,
                683,
                1217,
                2283,
                4095,
                4095
              ],
              [
                62,
                136,
                206,
                347,
                620,
                1178,
                2851
              ],
              [
                150,
                417,
                683,
                1217,
                2283,
                4095,
                4095
              ],
              [
                150,
                417,
                683,
                1217,
                2283,
                4095,
                4095
              ],
              [
                150,
                283,
                417,
                683,
                1217,
                2817,
                4095
              ]
            ],
            "detector_offsets": [
              6,
              0,
              10,
              0
            ],
            "par_tweak": 0.888
          }
        },
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
    "42.6911886",
    "-84.4464213"
  ],
  "time_offset": "America/Detroit"
}
