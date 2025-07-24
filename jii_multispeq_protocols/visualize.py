"""
Visualize the content of a protocol as a flowchart
"""

import json
import numpy as np
import gettext

DETECTORS = {
  "1": "700nm - 1150nm",
  "3": "400nm - 700nm (BG18)"
}

LEDS = {
  "1": "530nm (Main)",
  "2": "655nm (Main)",
  "3": "590nm (Main)",
  "4": "448nm (Main)",
  "5": "950nm (Main)",
  "6": "950nm (Clamp)",
  "7": "655nm (Clamp)",
  "8": "850nm (Clamp)",
  "9": "730nm (Clamp)",
  "10": "820nm (Clamp)"
}

SENSORS = {
  "temperature_humidity_pressure|temperature_humidity_pressure2|thp|thp2": "Ambient Temperature, Humidity, Pressure",
  "contactless_temp": "Contactless Temperature",
  "compass_and_angle": "Accelerometer & Magnetometer",
  "thickness|thickness_raw": "Hall Effect Sensor",
  "light_intensity|previous_light_intensity": "PAR light sensor"
}

JII_STYLES = {
  'primaryColor': '#49e06d',
  'primaryTextColor': '#005e5e',
  'primaryBorderColor': '#005e5e',
  'lineColor': '#fff381',
  'secondaryColor': '#afd7f4',
  'tertiaryColor': '#D7EBF9'
}

def start(element):
  """
  Get start signal
  """
  out = None

  if "start_on_open" in element and element["start_on_open"] == 1:
    out = "**Waits until**: Clamp opened"

  if "start_on_close" in element and element["start_on_close"] == 1:
    out = "**Waits until**: Clamp closed"

  if "open_close_start" in element and element["open_close_start"] == 1:
    out = "**Waits until**: Clamp opened and closed"

  if "start_on_open_close" in element and element["start_on_open_close"] == 1:
    out = "**Waits until**: Clamp opened and closed"
  
  if "par_led_start_on_open" in element:
    out = "**Waits until**: Clamp opened\n%s" % LEDS[str(element["par_led_start_on_open"])]

  if "par_led_start_on_close" in element:
    out = "**Waits until**: Clamp closed\n%s" % LEDS[str(element["par_led_start_on_close"])]

  if "par_led_start_on_open_close" in element:
    out = "**Waits until**: Clamp opened and closed\n%s" % LEDS[str(element["par_led_start_on_open_close"])]

  return out

def label(element, idx = -1):
  """
  Generate Label Name
  """
  out = "Protocol"

  if "label" in element:
    out = element["label"]

  if idx > -1 and "label" not in element:
    out = "Protocol #%s" % (idx+1)
    
  return out

def detectors(element):
  """
  Get Detectors
  """
  out = None

  if "detectors" in element:
    l = len(np.unique(np.hstack(element["detectors"])))
    out = np.unique(np.hstack(element["detectors"]))
    out = [DETECTORS[str(x)] for x in out if str(x) in DETECTORS]
    out = ("\n".join(out) if l == 1 else ("\n" + "\n".join(["• %s" % o for o in out])))

    out = out, len(np.unique(np.hstack(element["detectors"])))
    
  return out

def leds(element, lights="nonpulsed_lights"):
  """
  Get LEDs
  """
  out = None

  if lights in element:
    l = len(np.unique(np.hstack(element[lights])))
    out = np.unique(np.hstack(element[lights]))
    out = [LEDS[str(x)] for x in out if str(x) in LEDS]
    out = ("\n".join(out) if l == 1 else ("\n" + "\n".join(["• %s" % o for o in out])))

    out = out, l
    
  return out

def environment(element):
  """
  Get Sensors
  """
  out = None

  def matchSensor(input):
    for key,sensor in SENSORS.items():
      if input in key:
        return sensor
    return str(input)

  if "environmental" in element:
    l = len(np.unique(np.hstack(element["environmental"])))
    out = np.unique(np.hstack(element["environmental"]))
    out = np.unique([matchSensor(x) for x in out])
    out = ("\n".join(out) if l == 1 else ("\n" + "\n".join(["• %s" % o for o in out])))

    out = out, l
    
  return out

def preillumination(element, v_arr=None):
  """
  Get Pre-Illumination
  """
  out = None

  if "pre_illumination" in element:
    if isinstance(element["pre_illumination"], list):
      if isinstance(element["pre_illumination"][0], list):
        out = []
        for arr in element["pre_illumination"]:
          pos1 = get_variable(arr[1], v_arr)
          pos2 = get_variable(arr[2], v_arr)
          out.append("%s\n*Duration (ms)*: %s\n*PAR*: %s" % ( LEDS[str(arr[0])], pos1, pos2 ))
        out = "**Illumination**\n%s" % "\n".join(out)
      else:
        pos1 = get_variable(element["pre_illumination"][1], v_arr)
        pos2 = get_variable(element["pre_illumination"][2], v_arr)
        out = "**Illumination**\n%s\n*Duration (ms)*: %s\n*PAR*: %s" % ( LEDS[str(element["pre_illumination"][0])], pos1, pos2 )

  return out

def protocols(element):
  """
  Get Protocols repeat
  """
  out = None

  if "protocols" in element:
    out = element["protocols"]
    
  return out

def protocols_repeats(element):
  """
  Get Protocols repeat
  """
  out = None

  if "protocol_repeats" in element:
    out = element["protocol_repeats"]

  return out

def protocols_delay(element):
  """
  Get Protocol delay
  """
  out = None

  if "protocols_delay" in element:
    out = element["protocols_delay"]
    
  return out

def set_repeats(element):
  """
  Get Set Repeats
  """
  out = None

  if "set_repeats" in element:
    out = element["set_repeats"]

  return out

def do_once(element):
  """
  Get Do Once
  """
  out = None

  if "do_once" in element:
    if element["do_once"] == 1:
      out = "Runs only during *first* repeat"
    if element["do_once"] == -1:
      out = "Runs only during *last* repeat"

  return out

def averages(element):
  """
  Get Averages
  """
  out = None

  if "averages" in element:
    out = element["averages"]

  return out

def averages_delay(element):
  """
  Get Averages delay
  """
  out = None

  if "averages_delay" in element:
    out = element["averages_delay"]

  return out

def v_arrays(element):
  """
  Get variable arrays
  """
  out = None

  if "v_arrays" in element:
    out = element["v_arrays"]

  return out

def get_variable(variable, v_arr=None):
  """
  Get the content of a variable
  """
  out = variable

  if isinstance(variable, str) and v_arr is not None:
    
    if variable.startswith('#l'):
      idx = int(variable[2:])
      if idx < len(v_arr):
        out = len(v_arr[idx])

    if variable.startswith('@s'):
      idx = int(variable[2:])
      if idx < len(v_arr):
        out = ', '.join(map(str,v_arr[idx]))

    if variable.startswith('@p'):
      idx = int(variable[2:])
      if idx < len(v_arr):
        out = ', '.join(map(str,v_arr[idx]))

    if variable.startswith('@n'):
      idx = list(map(int, variable[2:].split(':') ))
      if idx[0] in range(len(v_arr)):
        if idx[1] in range(len(v_arr[idx[0]])):
          out = v_arr[idx[0]][idx[1]]

  return out


def content(element):
  """
  Generate Protocol Content
  """
  out = []
  ## Protocol Title
  out.append("**%s**" % (label(element)))

  ## Averages
  if averages(element):
    avg = averages(element)
    if isinstance(avg, int):
      if avg > 1:
        avg = "*Averages*: %s" % (avg)
        if averages_delay(element):
          avg += " (delay between: %s)" % (averages_delay(element))
        out.append(avg)

  ## Repeats
  if protocols_repeats(element):
    rep = protocols_repeats(element)
    if isinstance(rep, int):
      if rep > 1:
        rep = "*Repeats*: %s" % (rep)
        if protocols_delay(element):
          rep += " (delay between: %s)" % (protocols_delay(element))
        out.append(rep)

  ## Detectors
  if detectors(element):
    out.append("*%s:* %s" % ( gettext.ngettext( 'Detector', 'Detector', detectors(element)[1] ), detectors(element)[0]))

  ## LEDs
  if leds(element, "pulsed_lights"):
    out.append("*%s:* %s" % ( gettext.ngettext( 'Pulsed LED', 'Pulsed LEDs', leds(element,"pulsed_lights")[1] ), leds(element,"pulsed_lights")[0]))

  ## LEDs
  if leds(element, "nonpulsed_lights"):
    out.append("*%s:* %s" % ( gettext.ngettext( 'Non Pulsed LED', 'Non Pulsed LEDs', leds(element,"nonpulsed_lights")[1] ), leds(element,"nonpulsed_lights")[0]))

  ## Other Sensors
  if environment(element):
    out.append("*%s:* %s" % ( gettext.ngettext( 'Sensor', 'Sensors', environment(element)[1] ), environment(element)[0]) )

  ## Execution
  if do_once(element):
    out.append("%s" % do_once(element))

  return "\n".join(out)

def generate ( protocol = None, direction = 'TD', styles=None ):
  """
  Generate a flow chart for a given protocol using the Mermaid library.

  :param protocol: Protocol code to visualize
  :type protocol: str, dict or list

  :param direction: Flow-chart direction flow (TB, TD, BT, RL, LR)
  :type protocol: str

  :param style: Flow-chart styles (see: `Mermaid Theme Variables <https://mermaid.js.org/config/theming.html#customizing-themes-with-themevariables>`_ )
  :type protocol: dict

  :return: Flow chart code for Mermaid
  :rtype: str

  :raises ValueError: if no protocol data is provided or the protocol data has the wrong format
  :raises ValueError: if direction has incorrect value
  :raises ValueError: if style is not a dictinary
  """

  # TB - Top to bottom
  # TD - Top-down/ same as top to bottom
  # BT - Bottom to top
  # RL - Right to left
  # LR - Left to right

  if protocol is None:
    raise ValueError("No protocol provided to generate a flow-chart")
  
  if not isinstance(protocol, (str,dict,list)):
    raise ValueError("Provided protocol needs to be a dictionary, list or string")

  if not isinstance(direction, (str)):
    raise ValueError("Direction must be provided as a string")

  if styles is not None and not isinstance(styles, (dict)):
    raise ValueError("Styles must be provided as a dictionary")

  chart = ""
    
  if styles is not None:
    chart += f"""%%{{
init: {{
  "theme": "base",
  "themeVariables": {json.dumps(styles)}
}}
}}%%
"""

  ## Parse protocol string as json
  if isinstance(protocol, str):
    protocol = json.loads(protocol)

  ## In case protocol is a dict, turn it into a list
  if isinstance(protocol, dict):
    protocol = [protocol]

  ## Loop through protocols in list
  for element in protocol:

    chart += "flowchart %s\n" % direction
    
    ## Protocol Start
    chart += "\tSTART((Start))\n"
    
    if "_protocol_set_" in element:

      for idx, el in enumerate(element["_protocol_set_"]):
        
        ## Add Protocol Container
        chart += "\tA%s[\"`%s`\"]:::protocol\n" % (idx, content(el))

        ## Add connection between Sub-Protocols. Connection between previous and current is added.
        node = []
        
        ## Add Start/Interuptions.
        if start(el):
          node.append( start( el ) )

        ## Add pre-illumination.
        if preillumination(el):
          node.append( preillumination( el, v_arrays(element) ) )

        ## Add node connection
        chart += "\t%s ==>%s A%s\n" % ( ("A%s" % (idx-1) if idx > 0 else "START" ), ( "|\"`%s`\"|" % "\n\n".join(node) if len(node) > 0 else "" ), idx)

        ## Add End Point
        if idx == len(element["_protocol_set_"]) -1:
          if protocols_delay(el):
            chart += "\tA%s ==> |%sms| END\n" % (idx, protocols_delay(el))
          else:
            chart += "\tA%s ==> END\n" % idx


      ## Add set repeats
      if set_repeats(element):
        chart += "\tA%s -.-> |%sx| A0\n" % (idx, get_variable( set_repeats(element), v_arrays(element) ))
        
        ## change thickness of dotted line
        chart += "\tlinkStyle %s stroke-width:3px\n" % (idx+2)
    
    else:
      ## Protocol
      chart += "\tA0[\"`%s`\"]:::protocol\n" % content(element)

      node = []

      ## Add Start/Interuptions.
      if start( element ):
        node.append( start( element ) )

      ## Add pre-illumination.
      if preillumination( element ):
        node.append( preillumination( element ) )

      chart += "\tSTART ==>%s A0\n" % ( ( "|\"`%s`\"|" % "\n\n".join(node) if len(node) > 0 else "" ))

      chart += "\tA0 ==> END\n"

    ## Protocol End
    chart += "\tEND((&nbsp;End&nbsp;))\n"

    chart += "\tclassDef protocol text-align:left,white-space:pre;"

  return chart
