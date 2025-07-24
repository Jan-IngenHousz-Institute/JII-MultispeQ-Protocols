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

  # Return data
  return output

