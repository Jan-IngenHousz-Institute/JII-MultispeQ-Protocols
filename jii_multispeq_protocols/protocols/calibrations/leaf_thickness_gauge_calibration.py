"""
Leaf Thickness Gauge Calibration
================================

Description

The MultispeQ measures leaf thickness by using a Hall Effect sensor located on the main body of the MultispeQ and a magnet located on the clamp body. The Hall Effect sensor measures the density of magnetic field lines, and as the clamp opens and the magnet moves farther away, the field lines go farther apart. This extremely precise sensor is able to detect differences of 10s of microns given a consistent setup. Precision in the field is not that good, as dirt, bumps and veins in the leaf, and other noise can interfere.

Calibration of the Hall Effect sensor requires the measurement of objects of a few known thicknesses, and a calibration curve (2nd order polynomial fit) of the resulting Hall Effect detector response to the actual values.

In addition, the Hall Effect sensor is also used to identify fully closed and fully open positions, which is used to automatically start a measurement on clamp (the "open_close_start" command). This is used in the "Leaf Photosynthesis" protocol, for example. If you want to only recalibrate the fully open and fully closed positions, then run the "v1.0 CALIBRATION: Leaf Thickness Quick" calibration instead.

Directions

Run this protocol using the Desktop App (it is the only app which can currently display messages)
Make sure you have 6 plastic strips of known thickness (from .05 to 3mm).
Run the protocol, following the directions provided by the messages.
Once complete, press the "save to device" button to save the outputs to the MultispeQ device. If it is running as part of a Calibration Project (as during factory calibration), then press "keep" to save the values to the photosynq.org 1website.
As with any values saved to the MultispeQ, you can see the saved calibration values by opening the Desktop App, going to "Settings" --> "console", and entering print_memory+ . The leaf thickness values are saved as "thickness_a","thickness_b","thickness_c","thickness_min","thickness_max".


2232
"""

import numpy as np
from scipy import stats
from jii_multispeq.analysis import GetProtocolByLabel
import warnings

_protocol = [
  {
    "_protocol_set_": [
      {
        "label": "thick",
        "alert": "Leave the Leaf Clamp fully closed",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "prompt": "Clamp the ***Red*** Thickness Calibration Card or enter alternate value",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "prompt": "Clamp the ***Blue*** Thickness Calibration Card or enter alternate value",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "prompt": "Clamp the ***Translucent*** Thickness Calibration Card or enter alternate value",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "prompt": "Clamp the ***White*** Thickness Calibration Card or enter alternate value",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "prompt": "Clamp the ***Clear*** Thickness Calibration Card or enter alternate value",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "prompt": "Clamp the ***Black*** Thickness Calibration Card or enter alternate value",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      },
      {
        "label": "thick",
        "alert": "Leaf Clamp fully open",
        "environmental": [
          [
            "thickness_raw"
          ]
        ]
      }
    ]
  }
]

def _analyze( _data ):
  """
  Macro for calibrating leaf thickness in the MultispeQ v1.0
  created: 7/1/2018 
  """
    
  ## utilizes polynomial fit, using the MathPOLYREG(array,degrees)
  ## note that all values are converted to um for storage (since they are stored as floats, this helps reduce the number of very very small saved values which could be less than 6 numbers into the decimal place
  
  ## Define the output object here
  output = {}

  calibrationStandards = [50,125,190,650,1000,2500,11300]
  calibrationStandards = [0, 80,170,220,650,930,2400,11300]

  ## distances measured and replicates for each distance measured for this protocol
  thickCal = GetProtocolByLabel("thick", _data, True)
  distancesMeasured = len(thickCal)

  measuredHallVals = []
  for i in range(distancesMeasured):
    measuredHallVals.append(thickCal[i]["thickness_raw"])

  output["measuredHallVals"] = measuredHallVals
  output["calibrationStandards"] = calibrationStandards

  fitArray = [list(x) for x in zip(measuredHallVals[0:(distancesMeasured-1)], calibrationStandards[0:(distancesMeasured-1)])]
  output["fitArray"] = repr(fitArray)

  # polyfit = np.polyfit(*fitArray,2)
  polyfit = np.polyfit(measuredHallVals[0:(distancesMeasured-1)], calibrationStandards[0:(distancesMeasured-1)] ,2)
  coefficients = polyfit.tolist()
  thickness_a = np.round(coefficients[2],13)
  thickness_b = np.round(coefficients[1],7)
  thickness_c = np.round(coefficients[0],4)

  output["toDevice"] = "set_thickness+%s+%s+%s+%s+%s+" % ( (thickness_a*1000000000), thickness_b, thickness_c, measuredHallVals[0], measuredHallVals[distancesMeasured-1] )

  predictedThicknessVals = []
  residuals = []

  for i in range(distancesMeasured-1):
    thisThickness = measuredHallVals[i]
    thickness_predicted = np.round(thickness_a * thisThickness**2 + thickness_b*thisThickness + thickness_c, 0)
    predictedThicknessVals.append(thickness_predicted)
    residuals.append(thickness_predicted - calibrationStandards[i])

  output["predictedThicknessVals"] = predictedThicknessVals
  output["residuals"] = residuals

  slope, intercept, r_value, p_value, std_err = stats.linregress(calibrationStandards[0:(distancesMeasured-1)], predictedThicknessVals)
  output["r2"] = np.round(r_value**2, 3)
  output["slope"] = np.round(slope, 3)
  output["y_intercept"] = "%s mm" % np.round(intercept/1000,3)


  if output["r2"] < .95:
    msg = "r² value  for linear regression low (r² = %s, expected: >0.95), or linear regression failed. If the issue presists, your thickness calibration cards might need to be cleaned. Also make sure the leaf clamp opens and closes smoothly." % np.round(output["r2"],2) if output["r2"] else "failed"
    warnings.warn(msg)
  else:
    print("Leaf thickness calibration was successful")
    output["toDevice"] += "setCalTime+4+hello+"


  return output

_example = {
  "time": 1590074016885,
  "device_name": "MultispeQ",
  "device_version": "2",
  "device_id": "32:21:3c:e5",
  "device_battery": 106,
  "device_firmware": 2.191,
  "sample": [
    [
      {
        "time": 1590074016885,
        "protocol_id": 1,
        "set": [
          {
            "time": 1590074022915,
            "data_raw_size": "0",
            "message": [
              "alert",
              "thickness fully closed",
              "ok"
            ],
            "label": "thick",
            "thickness_raw": 53199,
            "data_raw": [

            ]
          },
          {
            "time": 1590074025535,
            "data_raw_size": "0",
            "message": [
              "prompt",
              "thickness Card 2 (red) or enter alternate value",
              ""
            ],
            "label": "thick",
            "thickness_raw": 52839,
            "data_raw": [

            ]
          },
          {
            "time": 1590074032377,
            "data_raw_size": "0",
            "message": [
              "prompt",
              "thickness Card 3 (blue) or enter alternate value",
              ""
            ],
            "label": "thick",
            "thickness_raw": 52376,
            "data_raw": [

            ]
          },
          {
            "time": 1590074036911,
            "data_raw_size": "0",
            "message": [
              "prompt",
              "thickness Card 4 (translucent) or enter alternate value",
              ""
            ],
            "label": "thick",
            "thickness_raw": 51730,
            "data_raw": [

            ]
          },
          {
            "time": 1590074041184,
            "data_raw_size": "0",
            "message": [
              "prompt",
              "thickness Card 5 (White) or enter alternate value",
              ""
            ],
            "label": "thick",
            "thickness_raw": 48480,
            "data_raw": [

            ]
          },
          {
            "time": 1590074046184,
            "data_raw_size": "0",
            "message": [
              "prompt",
              "thickness Card 6 (Clear) or enter alternate value",
              ""
            ],
            "label": "thick",
            "thickness_raw": 47055,
            "data_raw": [

            ]
          },
          {
            "time": 1590074051137,
            "data_raw_size": "0",
            "message": [
              "prompt",
              "thickness Card 7 (Black) or enter alternate value",
              ""
            ],
            "label": "thick",
            "thickness_raw": 42525,
            "data_raw": [

            ]
          },
          {
            "time": 1590074055107,
            "data_raw_size": "0",
            "message": [
              "alert",
              "clamp fully open",
              "ok"
            ],
            "label": "thick",
            "thickness_raw": 38517,
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
  "location": False,
  "time_offset": "America/Detroit"
}