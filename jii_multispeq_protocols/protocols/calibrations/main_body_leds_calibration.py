"""
Main Body LEDs Calibration
==========================

new version of CaliQ LED output calibration using PAR matching...

.. warning:: This calibration requires a CaliQ

2280
"""

import numpy as np
from scipy import stats
from jii_multispeq.analysis import GetProtocolByLabel

_protocol = [
  {
    "v_arrays": [
      [
        1200,
        20000,
        1500,
        12000
      ],
      [
        40,
        600
      ],
      [
        600,
        1200
      ],
      [
        40,
        600,
        3000
      ],
      [
        600,
        3000,
        9000
      ],
      [
        50,
        300
      ],
      [
        300,
        500
      ],
      [
        40,
        600,
        3000
      ],
      [
        600,
        3000,
        9000
      ]
    ],
    "set_repeats": 1,
    "_protocol_set_": [
      {
        "label": "cal_led_1",
        "qpar_led_cal": [
          1,
          "@p1",
          "@p2",
          20
        ],
        "protocol_repeats": "#l1"
      },
      {
        "label": "cal_led_2",
        "qpar_led_cal": [
          2,
          "@p3",
          "@p4",
          20
        ],
        "protocol_repeats": "#l3"
      },
      {
        "label": "cal_led_3",
        "qpar_led_cal": [
          3,
          "@p5",
          "@p6",
          20
        ],
        "protocol_repeats": "#l5"
      },
      {
        "label": "cal_led_4",
        "qpar_led_cal": [
          4,
          "@p7",
          "@p8",
          20
        ],
        "protocol_repeats": "#l7"
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

  ## The MultispeQ uses the following fixed PAR values
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
      
      for i in range( len(led2[set_number]["qpar_led_cal"]) ):
        if led2[set_number]["qpar_led_cal"][i][1] > 0:
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
  "time": "1629320993633",
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "31:f4:e8:4d",
  "device_battery": 63,
  "device_firmware": 2.345,
  "sample": [
    [
      {
        "time": "1629320993635",
        "v_arrays": [
          [
            1200,
            20000,
            1500,
            12000
          ],
          [
            40,
            600
          ],
          [
            600,
            1200
          ],
          [
            40,
            600,
            3000
          ],
          [
            600,
            3000,
            9000
          ],
          [
            50,
            300
          ],
          [
            300,
            500
          ],
          [
            40,
            600,
            3000
          ],
          [
            600,
            3000,
            9000
          ]
        ],
        "set_repeats": 1,
        "protocol_id": "editor",
        "set": [
          {
            "time": "1629320993656",
            "led_to_qpar0": [
              1,
              40,
              74.01,
              75
            ],
            "led_to_qpar1": [
              1,
              600,
              647.17,
              267
            ],
            "qpar_led_cal": [
              [
                75,
                40
              ],
              [
                84,
                90
              ],
              [
                93,
                119
              ],
              [
                102,
                131
              ],
              [
                111,
                172
              ],
              [
                120,
                189
              ],
              [
                129,
                208
              ],
              [
                138,
                249
              ],
              [
                147,
                266
              ],
              [
                156,
                295
              ],
              [
                165,
                326
              ],
              [
                174,
                347
              ],
              [
                183,
                382
              ],
              [
                192,
                412
              ],
              [
                201,
                428
              ],
              [
                210,
                471
              ],
              [
                219,
                488
              ],
              [
                228,
                511
              ],
              [
                237,
                551
              ],
              [
                246,
                570
              ],
              [
                255,
                602
              ],
              [
                264,
                630
              ]
            ],
            "label": "cal_led_1",
            "data_raw": [

            ]
          },
          {
            "time": "1629321017842",
            "led_to_qpar0": [
              1,
              600,
              657.19,
              267
            ],
            "led_to_qpar1": [
              1,
              1200,
              1585.55,
              567
            ],
            "qpar_led_cal": [
              [
                267,
                389
              ],
              [
                282,
                677
              ],
              [
                297,
                736
              ],
              [
                312,
                766
              ],
              [
                327,
                827
              ],
              [
                342,
                871
              ],
              [
                357,
                899
              ],
              [
                372,
                972
              ],
              [
                387,
                1005
              ],
              [
                402,
                1036
              ],
              [
                417,
                1110
              ],
              [
                432,
                1140
              ],
              [
                447,
                1198
              ],
              [
                462,
                1247
              ],
              [
                477,
                1276
              ],
              [
                492,
                1354
              ],
              [
                507,
                1385
              ],
              [
                522,
                1424
              ],
              [
                537,
                1491
              ],
              [
                552,
                1520
              ],
              [
                567,
                1573
              ],
              [
                582,
                1625
              ]
            ],
            "label": "cal_led_1",
            "data_raw": [

            ]
          },
          {
            "time": "1629321044494",
            "led_to_qpar0": [
              2,
              40,
              0,
              50
            ],
            "led_to_qpar1": [
              2,
              600,
              817.4,
              315
            ],
            "qpar_led_cal": [
              [
                50,
                0
              ],
              [
                63,
                4
              ],
              [
                76,
                17
              ],
              [
                89,
                64
              ],
              [
                102,
                89
              ],
              [
                115,
                108
              ],
              [
                128,
                182
              ],
              [
                141,
                208
              ],
              [
                154,
                268
              ],
              [
                167,
                300
              ],
              [
                180,
                330
              ],
              [
                193,
                395
              ],
              [
                206,
                425
              ],
              [
                219,
                469
              ],
              [
                232,
                527
              ],
              [
                245,
                555
              ],
              [
                258,
                623
              ],
              [
                271,
                659
              ],
              [
                284,
                683
              ],
              [
                297,
                753
              ],
              [
                310,
                781
              ],
              [
                323,
                822
              ]
            ],
            "label": "cal_led_2",
            "data_raw": [

            ]
          },
          {
            "time": "1629321074822",
            "led_to_qpar0": [
              2,
              600,
              672.2,
              267
            ],
            "led_to_qpar1": [
              2,
              3000,
              3564.23,
              1062
            ],
            "qpar_led_cal": [
              [
                267,
                664
              ],
              [
                306,
                758
              ],
              [
                345,
                860
              ],
              [
                384,
                1068
              ],
              [
                423,
                1155
              ],
              [
                462,
                1294
              ],
              [
                501,
                1474
              ],
              [
                540,
                1563
              ],
              [
                579,
                1651
              ],
              [
                618,
                1875
              ],
              [
                657,
                1966
              ],
              [
                696,
                2190
              ],
              [
                735,
                2283
              ],
              [
                774,
                2417
              ],
              [
                813,
                2601
              ],
              [
                852,
                2691
              ],
              [
                891,
                2872
              ],
              [
                930,
                3022
              ],
              [
                969,
                3112
              ],
              [
                1008,
                3341
              ],
              [
                1047,
                3446
              ],
              [
                1086,
                3557
              ]
            ],
            "label": "cal_led_2",
            "data_raw": [

            ]
          },
          {
            "time": "1629321101474",
            "led_to_qpar0": [
              2,
              3000,
              3571.28,
              1062
            ],
            "led_to_qpar1": [
              2,
              9000,
              12641.5,
              3434
            ],
            "qpar_led_cal": [
              [
                1062,
                636
              ],
              [
                1180,
                4056
              ],
              [
                1298,
                4317
              ],
              [
                1416,
                5023
              ],
              [
                1534,
                5304
              ],
              [
                1652,
                5721
              ],
              [
                1770,
                6312
              ],
              [
                1888,
                6603
              ],
              [
                2006,
                7157
              ],
              [
                2124,
                7623
              ],
              [
                2242,
                7913
              ],
              [
                2360,
                8639
              ],
              [
                2478,
                8941
              ],
              [
                2596,
                9305
              ],
              [
                2714,
                10010
              ],
              [
                2832,
                10277
              ],
              [
                2950,
                10826
              ],
              [
                3068,
                11421
              ],
              [
                3186,
                11808
              ],
              [
                3304,
                12439
              ],
              [
                3422,
                12606
              ],
              [
                3540,
                12820
              ]
            ],
            "label": "cal_led_2",
            "data_raw": [

            ]
          },
          {
            "time": "1629321137130",
            "led_to_qpar0": [
              3,
              50,
              5.78,
              50
            ],
            "led_to_qpar1": [
              3,
              300,
              299.28,
              708
            ],
            "qpar_led_cal": [
              [
                50,
                2
              ],
              [
                82,
                21
              ],
              [
                114,
                31
              ],
              [
                146,
                44
              ],
              [
                178,
                68
              ],
              [
                210,
                78
              ],
              [
                242,
                97
              ],
              [
                274,
                117
              ],
              [
                306,
                128
              ],
              [
                338,
                147
              ],
              [
                370,
                162
              ],
              [
                402,
                172
              ],
              [
                434,
                198
              ],
              [
                466,
                204
              ],
              [
                498,
                216
              ],
              [
                530,
                233
              ],
              [
                562,
                245
              ],
              [
                594,
                254
              ],
              [
                626,
                268
              ],
              [
                658,
                273
              ],
              [
                690,
                288
              ],
              [
                722,
                295
              ]
            ],
            "label": "cal_led_3",
            "data_raw": [

            ]
          },
          {
            "time": "1629321160913",
            "led_to_qpar0": [
              3,
              300,
              302.69,
              708
            ],
            "led_to_qpar1": [
              3,
              500,
              469.76,
              1593
            ],
            "qpar_led_cal": [
              [
                708,
                212
              ],
              [
                752,
                276
              ],
              [
                796,
                304
              ],
              [
                840,
                313
              ],
              [
                884,
                320
              ],
              [
                928,
                339
              ],
              [
                972,
                340
              ],
              [
                1016,
                338
              ],
              [
                1060,
                361
              ],
              [
                1104,
                361
              ],
              [
                1148,
                372
              ],
              [
                1192,
                373
              ],
              [
                1236,
                374
              ],
              [
                1280,
                383
              ],
              [
                1324,
                380
              ],
              [
                1368,
                380
              ],
              [
                1412,
                382
              ],
              [
                1456,
                382
              ],
              [
                1500,
                381
              ],
              [
                1544,
                380
              ],
              [
                1588,
                375
              ],
              [
                1632,
                371
              ]
            ],
            "label": "cal_led_3",
            "data_raw": [

            ]
          },
          {
            "time": "1629321180197",
            "led_to_qpar0": [
              4,
              40,
              0,
              50
            ],
            "led_to_qpar1": [
              4,
              600,
              704.31,
              252
            ],
            "qpar_led_cal": [
              [
                50,
                0
              ],
              [
                60,
                0
              ],
              [
                70,
                0
              ],
              [
                80,
                0
              ],
              [
                90,
                0
              ],
              [
                100,
                0
              ],
              [
                110,
                4
              ],
              [
                120,
                22
              ],
              [
                130,
                52
              ],
              [
                140,
                111
              ],
              [
                150,
                140
              ],
              [
                160,
                208
              ],
              [
                170,
                255
              ],
              [
                180,
                289
              ],
              [
                190,
                368
              ],
              [
                200,
                406
              ],
              [
                210,
                449
              ],
              [
                220,
                529
              ],
              [
                230,
                560
              ],
              [
                240,
                620
              ],
              [
                250,
                683
              ],
              [
                260,
                717
              ]
            ],
            "label": "cal_led_4",
            "data_raw": [

            ]
          },
          {
            "time": "1629321210522",
            "led_to_qpar0": [
              4,
              600,
              1043.74,
              315
            ],
            "led_to_qpar1": [
              4,
              3000,
              3343.39,
              708
            ],
            "qpar_led_cal": [
              [
                315,
                848
              ],
              [
                334,
                1088
              ],
              [
                353,
                1247
              ],
              [
                372,
                1319
              ],
              [
                391,
                1394
              ],
              [
                410,
                1545
              ],
              [
                429,
                1606
              ],
              [
                448,
                1708
              ],
              [
                467,
                1833
              ],
              [
                486,
                1896
              ],
              [
                505,
                2030
              ],
              [
                524,
                2122
              ],
              [
                543,
                2186
              ],
              [
                562,
                2337
              ],
              [
                581,
                2398
              ],
              [
                600,
                2487
              ],
              [
                619,
                2610
              ],
              [
                638,
                2674
              ],
              [
                657,
                2785
              ],
              [
                676,
                2882
              ],
              [
                695,
                2940
              ],
              [
                714,
                3090
              ]
            ],
            "label": "cal_led_4",
            "data_raw": [

            ]
          },
          {
            "time": "1629321235942",
            "led_to_qpar0": [
              4,
              3000,
              4745.81,
              1062
            ],
            "led_to_qpar1": [
              4,
              9000,
              10300.67,
              2390
            ],
            "qpar_led_cal": [
              [
                1062,
                3925
              ],
              [
                1128,
                4976
              ],
              [
                1194,
                5164
              ],
              [
                1260,
                5637
              ],
              [
                1326,
                5828
              ],
              [
                1392,
                6073
              ],
              [
                1458,
                6481
              ],
              [
                1524,
                6660
              ],
              [
                1590,
                6976
              ],
              [
                1656,
                7291
              ],
              [
                1722,
                7465
              ],
              [
                1788,
                7895
              ],
              [
                1854,
                8086
              ],
              [
                1920,
                8277
              ],
              [
                1986,
                8694
              ],
              [
                2052,
                8866
              ],
              [
                2118,
                9141
              ],
              [
                2184,
                9465
              ],
              [
                2250,
                9625
              ],
              [
                2316,
                9973
              ],
              [
                2382,
                10208
              ],
              [
                2448,
                10367
              ]
            ],
            "label": "cal_led_4",
            "data_raw": [

            ]
          }
        ],
        "data_raw": [

        ]
      }
    ]
  ],
  "app_os": "macOS 18.7.0",
  "app_name": "PhotosynQ",
  "app_version": "1.10.59",
  "app_device": "x64",
  "location": False,
  "time_offset": "America/Detroit",
  "protocol": "[{\"v_arrays\":[[1200,20000,1500,12000],[40,600],[600,1200],[40,600,3000],[600,3000,9000],[50,300],[300,500],[40,600,3000],[600,3000,9000]],\"set_repeats\":1,\"_protocol_set_\":[{\"label\":\"cal_led_1\",\"qpar_led_cal\":[1,\"@p1\",\"@p2\",20],\"protocol_repeats\":\"#l1\"},{\"label\":\"cal_led_2\",\"qpar_led_cal\":[2,\"@p3\",\"@p4\",20],\"protocol_repeats\":\"#l3\"},{\"label\":\"cal_led_3\",\"qpar_led_cal\":[3,\"@p5\",\"@p6\",20],\"protocol_repeats\":\"#l5\"},{\"label\":\"cal_led_4\",\"qpar_led_cal\":[4,\"@p7\",\"@p8\",20],\"protocol_repeats\":\"#l7\"}],\"protocol_id\":2280}]"
}