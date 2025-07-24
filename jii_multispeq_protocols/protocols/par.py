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
        "light_intensity"
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

  output['PAR'] = _data['light_intensity']
  output['red'] = _data['r']
  output['green'] = _data['g']
  output['blue'] = _data['b']

  return output

_example = {
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "01:12:53:20",
  "device_battery": 82,
  "device_firmware": 2.3465,
  "sample": [
    {
      "ri": [
        0,
        415
      ],
      "protocol_id": "",
      "light_intensity": 346.791,
      "r": 2086.0,
      "g": 575.4,
      "b": 465.0,
      "w": 2863.6,
      "data_raw": []
    }
  ]
}
