"""
Photosynthetically Active Radiation (PAR)
=========================================

Use the MultispeQ's PAR sensor to measure light intensity (400-700nm)
in µmol photons × s⁻¹ × m⁻², which represents the Photosynthetically 
Active Radiation.

This protocol outputs the PAR value, as well as the raw values for
the red, green, and blue channel of the sensor.

"""

_protocol = [
  {
    "averages": 1,
    "environmental": [
      [
        "light_intensity",
        0
      ]
    ]
  }
]

def _analyze ( _data ):
  """
  Return the PAR value, as well as the RGB channels raw values.
  """

  # Define the output dictionary here
  output = {}

  output['PAR'] = _data['light_intesity']
  output['red'] = _data['r']
  output['green'] = _data['g']
  output['blue'] = _data['b']

  return output