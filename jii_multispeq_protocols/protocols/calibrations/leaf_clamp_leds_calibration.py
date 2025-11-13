"""
Leaf Clamp LEDs Calibration
===========================

new version of CaliQ LED output calibration using PAR matching...

qpar matching 1
testing CaliQ step 4 Calibrate LOWER PAR LEDs

.. warning:: This calibration requires a CaliQ

2279

"""

import numpy as np
from scipy import stats
from jii_multispeq.analysis import GetProtocolByLabel

_protocol = [
  {
    "v_arrays": [
      [
        6000
      ],
      [
        25,
        600,
        3000
      ],
      [
        600,
        3000,
        6000
      ]
    ],
    "set_repeats": 1,
    "_protocol_set_": [
      {
        "label": "cal_led_7",
        "qpar_led_cal": [
          7,
          "@p1",
          "@p2",
          20
        ],
        "protocol_repeats": "#l1"
      }
    ]
  }
]

def _analyze( _data ):
  """
  * Macro for data evaluation on PhotosynQ.org
  * by: David M. Kramer
  * created: July 17, 2020 10:10 AM
  """

  ## Define the output object here
  output = {}

  ## THe MultispeQ uses the following fixed PAR values
  ## as reference points for linear interpolation of the 
  ## DAC settings for desired PAR values.

  set_points = [0,150,300,600,1200,3000,6000,10000]

  ## Check if the key time exists in json
  if "time" in _data:
    ## Add key time and value to output
    output["time"] = _data["time"]

  all_labels = []
  _set = _data["set"]
  output["toDevice"] = ""
  
  for i in range(len(_set)):
    if "label" in _set[i]:
      if "cal_led_" in _set[i]["label"]:
        all_labels.append(_set[i]["label"])

  unique_LEDs = list( set(all_labels) )
  v_arrays = _data["v_arrays"]

  max_allowed_par = v_arrays[0]

  output["max_allowed_par"] = repr(max_allowed_par)
          
  output["toDevice"] = ""

  for led_index, _ in enumerate(unique_LEDs):
    led_label = unique_LEDs[led_index]
    set_number = 0
    led2 = GetProtocolByLabel(led_label, _data, True)
    LED = led2[0]["led_to_qpar0"][0]

    all_settings = []
    all_amplitudes = []
    all_slopes=[]
    all_b = []

    for set_number, _ in enumerate(led2):
      fit_points = []
      settings = []
      
      for i in range(1, len(led2[set_number]["qpar_led_cal"])):
        fit_points.append(led2[set_number]["qpar_led_cal"][i][1])
        settings.append(led2[set_number]["qpar_led_cal"][i][0])
              
      all_settings.append(settings)
      all_amplitudes.append(fit_points)

      slope, intercept, r_value, p_value, std_err = stats.linregress(fit_points, settings)
      output[("r2_%s:%s") % (led_label,set_number)] = np.round(r_value**2, 4)
      all_b.append(intercept)
      all_slopes.append(slope)
              
    ## find the ranges over which each equation applies.
    ## there should be n+2 ranges, where n is the number of entries
    ## in the v_arrays. 
    
    ## PAR = 0 to PAR = element 0
    ## element 0 to element 1
    ## ...
    ## last element to PAR = 10,000
    ## BUT, these 
    
    par_ranges = []
            
    lower_bounds_ranges = led_index * 2 + 1
    upper_bounds_ranges = led_index * 2 + 2 
    
    par_ranges.append([0,v_arrays[lower_bounds_ranges][0]])

    for range_index in range( len(v_arrays[lower_bounds_ranges])):
      par_ranges.append([v_arrays[lower_bounds_ranges][range_index], v_arrays[upper_bounds_ranges][range_index]])
    
    par_ranges.append([v_arrays[upper_bounds_ranges][len(v_arrays[upper_bounds_ranges]) -1], max_allowed_par[led_index]])

    set_point_values = []
    set_point_indexes = []
    set_points_to_fit = []
      
    ## The set point for dark (PAR=0) is jus the Y-intercept for the 
    ## first series of LED PAR vs. settings set.
    set_point_values.append(np.round(all_b[0]-1,0))
      
    ## The maximum setting is that for the max_allowed_par, using the 
    ## final (highest) LED PAR versus setting curve.
    
    max_par_range_index = len(all_slopes) - 1
    
    m = all_slopes[max_par_range_index]
    b = all_b[max_par_range_index]
    max_calibrated_setpoint = np.round(m * max_allowed_par[led_index] + b,0)
    if max_calibrated_setpoint > 4095:
      max_calibrated_setpoint=4095
    
    if max_calibrated_setpoint < 0:
      max_calibrated_setpoint=0
    
    output["max_setpoint_for_led:%s" % led_index] =  np.round(max_calibrated_setpoint,0)
    
    ## Go through the remainting set points and determine which line to use
    ## for estimating the setting value.
    for set_point_index in range(1, len(set_points)):
      set_point_par = set_points[set_point_index] ## the PAR value we are trying to fit.
      set_points_to_fit.append(set_point_par)
      
      ## go through each PAR range and find the one that fits
      for par_range_index,_ in enumerate(par_ranges):

        if set_point_par >= max_allowed_par[led_index]: 
          set_point_values.append(max_calibrated_setpoint)
          set_point_indexes.append(par_range_index)
          break
        elif set_point_par >= par_ranges[par_range_index][0]:
          set_point_indexes.append(par_range_index)
          m = all_slopes[par_range_index]
          b = all_b[par_range_index]
          calibrated_setpoint = m * set_point_par + b
          set_point_values.append(np.round(calibrated_setpoint,0))
          break
            
    output["toDevice"] += "par_to_dac_lin+%s+" % LED
    for cal_index in range(len(set_point_values)):
      output["toDevice"] += "%s+" % set_point_values[cal_index]
    
    output["toDevice"] += "par_max_setting+%s+%s+" % (LED, max_calibrated_setpoint)
        
  ## end of led loop

  ## Return data
  return output

_example = {
  "time": 1598118193361,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "41:00:08:6b",
  "device_battery": 101,
  "device_firmware": 2.3432,
  "sample": [
    [
      {
        "time": 1598118193361,
        "v_arrays": [
          [
            6000
          ],
          [
            25,
            600,
            3000
          ],
          [
            600,
            3000,
            6000
          ]
        ],
        "set_repeats": 1,
        "protocol_id": 1,
        "set": [
          {
            "time": 1598118193376,
            "led_to_qpar0": [
              7,
              25,
              0,
              50
            ],
            "led_to_qpar1": [
              7,
              600,
              964.81,
              472
            ],
            "qpar_led_cal": [
              [
                50,
                0
              ],
              [
                71,
                2
              ],
              [
                92,
                48
              ],
              [
                113,
                80
              ],
              [
                134,
                111
              ],
              [
                155,
                150
              ],
              [
                176,
                220
              ],
              [
                197,
                253
              ],
              [
                218,
                291
              ],
              [
                239,
                370
              ],
              [
                260,
                403
              ],
              [
                281,
                445
              ],
              [
                302,
                521
              ],
              [
                323,
                553
              ],
              [
                344,
                597
              ],
              [
                365,
                676
              ],
              [
                386,
                711
              ],
              [
                407,
                796
              ],
              [
                428,
                832
              ],
              [
                449,
                868
              ],
              [
                470,
                955
              ],
              [
                491,
                993
              ]
            ],
            "label": "cal_led_7",
            "data_raw": [

            ]
          },
          {
            "time": 1598118224113,
            "led_to_qpar0": [
              7,
              600,
              0,
              50
            ],
            "led_to_qpar1": [
              7,
              3000,
              3970.15,
              1593
            ],
            "qpar_led_cal": [
              [
                50,
                0
              ],
              [
                127,
                67
              ],
              [
                204,
                233
              ],
              [
                281,
                466
              ],
              [
                358,
                592
              ],
              [
                435,
                799
              ],
              [
                512,
                1050
              ],
              [
                589,
                1177
              ],
              [
                666,
                1389
              ],
              [
                743,
                1642
              ],
              [
                820,
                1774
              ],
              [
                897,
                1991
              ],
              [
                974,
                2246
              ],
              [
                1051,
                2390
              ],
              [
                1128,
                2605
              ],
              [
                1205,
                2861
              ],
              [
                1282,
                3003
              ],
              [
                1359,
                3222
              ],
              [
                1436,
                3485
              ],
              [
                1513,
                3626
              ],
              [
                1590,
                3864
              ],
              [
                1667,
                4141
              ]
            ],
            "label": "cal_led_7",
            "data_raw": [

            ]
          },
          {
            "time": 1598118256069,
            "led_to_qpar0": [
              7,
              3000,
              3995.94,
              1593
            ],
            "led_to_qpar1": [
              7,
              6000,
              7802.95,
              2876
            ],
            "qpar_led_cal": [
              [
                1593,
                1986
              ],
              [
                1657,
                4173
              ],
              [
                1721,
                4376
              ],
              [
                1785,
                4491
              ],
              [
                1849,
                4695
              ],
              [
                1913,
                4889
              ],
              [
                1977,
                4997
              ],
              [
                2041,
                5209
              ],
              [
                2105,
                5421
              ],
              [
                2169,
                5539
              ],
              [
                2233,
                5746
              ],
              [
                2297,
                5965
              ],
              [
                2361,
                6088
              ],
              [
                2425,
                6292
              ],
              [
                2489,
                6496
              ],
              [
                2553,
                6637
              ],
              [
                2617,
                6863
              ],
              [
                2681,
                7046
              ],
              [
                2745,
                7198
              ],
              [
                2809,
                7492
              ],
              [
                2873,
                7769
              ],
              [
                2937,
                7858
              ]
            ],
            "label": "cal_led_7",
            "data_raw": [

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
    "42.6912313",
    "-84.4464580"
  ],
  "time_offset": "America/Detroit"
}