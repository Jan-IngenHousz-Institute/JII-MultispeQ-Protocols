"""
Relative Chlorophyll Content (SPAD)
===================================

This protocol measures basic absorbance at 650 nm and 940 nm and calculates
the relative chlorophyll content.

The value returned represents the Special Products Analysis Division (SPAD)
to make it comparable to other instruments used in the field.

:math:`SPAD = k \\times \\log_{10}\\frac{Abs_{940nm} / ref. Abs_{940}}{Abs_{650nm} / ref. Abs_{650}}`

:math:`k` is a proprietary correlation coefficient used in the Minolta's
calculation of SPAD.

.. note:: Only works with MultispeQ v2.0

"""

_protocol = [
  {
    "_protocol_set_": [
      {
        "label": "spad",
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

def _analyze ( data ):
  """
  Macro for data evaluation on PhotosynQ.org
  by: David M. Kramer
  created: 2017-06-21 @ 10:36:29
  """

  # Define the output dictionary here
  output = {}

  output["spad"] = data.set[0].spad[0]
  
  return output
  