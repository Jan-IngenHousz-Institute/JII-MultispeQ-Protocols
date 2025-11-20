"""
Photosystem II efficiency (ϕₗₗ)
===============================

Basic protocol to measure the Photosystem II efficiency called phi2 or :math:`\Phi_{II}`. 
From the fluorescence trace several more values are produced, including
:math:`F_{S}`, the steady state fluorescence, :math:`F_{M}`, the maximum fluorescence, and LEF,
the linear electron flow, based on phi2 and the ambient light intensity.

"""

import numpy as np

_protocol = [
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
        "pulsed_lights": [
            [ 3 ], [ 3 ], [ 3 ]
        ],
        "pulsed_lights_brightness": [
            [ 2000 ], [ 2000 ], [ 2000 ]
        ],
        "nonpulsed_lights": [
            [ 2 ], [ 2 ], [ 2 ]
        ],
        "nonpulsed_lights_brightness": [
            [ "light_intensity" ], [ 4500 ], [ "light_intensity" ]
        ],
        "detectors": [
            [ 1 ], [ 1 ], [ 1 ]
        ],
        "environmental": [
            [ "light_intensity" ]
        ],
        "open_close_start": 1
    }
]

def _analyze ( _data ):
  """
  Macro for data evaluation on PhotosynQ.org
  by: John Doe
  created: June 4, 2018 4:00 PM
  """

  # Define the output dictionary here
  output = {}
  
  fs = np.mean(_data['data_raw'][1:5])
  fmp = np.mean( _data['data_raw'][63:68])
  phi2 = (fmp-fs)/fmp
  lef = phi2 * _data['light_intensity'] * 0.45

  output['Fs'] = fs
  output['Fmp'] = fmp
  output['Phi2'] = phi2
  output['LEF'] = lef
  output['PAR'] = _data['light_intensity']
  output['Fluorescence Trace'] = _data['data_raw']

  # Return data
  return output

_example = {
  "time": 1501283341143,
  "device_name": "MultispeQ",
  "device_version": "1",
  "device_id": "00:00:00:01",
  "device_battery": 100,
  "device_firmware": 1.2,
  "sample": [
    [
      {
        "time": 1501283341154,
        "label": "",
        "light_intensity": 17.95,
        "r": 15,
        "g": 7,
        "b": 4,
        "light_intensity_raw": 26,
        "data_raw": [
          15064,
          15232,
          15307,
          15334,
          15353,
          15351,
          15350,
          15341,
          15330,
          15331,
          15317,
          15315,
          15310,
          15298,
          15298,
          15290,
          15293,
          15289,
          15279,
          15280,
          20357,
          20671,
          20781,
          20838,
          20870,
          20894,
          20910,
          20924,
          20935,
          20953,
          20957,
          20958,
          20966,
          20974,
          20975,
          20978,
          20983,
          20986,
          20987,
          20992,
          20990,
          20996,
          20996,
          20991,
          20988,
          20991,
          20996,
          20993,
          20991,
          20985,
          20985,
          20983,
          20981,
          20977,
          20974,
          20971,
          20966,
          20965,
          20961,
          20960,
          20954,
          20951,
          20943,
          20943,
          20933,
          20931,
          20930,
          20922,
          20921,
          20912,
          19360,
          18530,
          18110,
          17863,
          17695,
          17565,
          17448,
          17349,
          17263,
          17171,
          17082,
          17006,
          16932,
          16851,
          16786,
          16715,
          16649,
          16594,
          16534,
          16471
        ]
      }
    ]
  ]
}