import json
import os
import warnings
import jii_multispeq_protocols

from string import Template

DEV = False

BODY = """Syntax
======

.. admonition:: Automatically Generated

   This part of the documentation is automatically generated from the schema file used for validating protocols following the 
   `2020-12 draft <$href>`_. For more detailed information on protocols, please refer the documentation by
   `PhotosynQ, Inc. <https://help.photosynq.com>`_

$commands

Definitions
-----------

**Array**
  In Python, "array" is analogous to the ``list`` or ``tuple`` type, depending on usage.

**Boolean**
  In Python, "boolean" is analogous to ``bool``. Note that in JSON, ``true`` and ``false`` are lower case, whereas in Python they are capitalized (``True`` and ``False``).

**Integer**
  In Python, "integer" is analogous to the ``int`` type.

**Dependencies**
   When a command has dependencies, all dependent commands have to be used as well for a valid protocol and to ensure proper function.

**Null**
  In Python, ``null`` is analogous to ``None``.

**Number**
  The ``number`` type is used for any numeric type, either ``integers`` or ``floating point`` numbers (``int`` or ``float`` in Python).

**Object**
  In Python, "objects" are analogous to the ``dict`` type. An important difference, however, is that while Python dictionaries may use anything hashable as a key, in JSON all the keys must be strings.

**String**
  The ``string`` type, in Python ``str`` is used for strings of text. It may contain Unicode characters.
"""


COMMAND = """
$commandname
$title_underline

$description

$example

.. rst-class:: inline-style-none

$config

$dependencies
"""

EXAMPLE = """
.. code-block:: python

$code

"""

def schema_to_rst():
  
  ## Schema file path
  file_path = os.path.join( os.path.dirname(jii_multispeq_protocols.__file__), 'schema.json' )

  ## Load schema file as JSON
  try:
    with open( file_path, 'r', encoding='utf-8') as fp:
      schema = json.load( fp )
  except json.JSONDecodeError:
    warnings.warn('Error: Invalid JSON (%s)' % file_path )
    schema = {}
    pass

  ## Get all commands from protocol (MultispeQ specific)
  cmds = schema["$defs"]["protocol"]["properties"].keys()

  ## List with rst formatted commands
  rst_cmds = []
  
  for cmd in cmds:
    details = schema["$defs"]["protocol"]["properties"][cmd]

    ## Command's main description
    description = ""
    if 'description' in details:
      description = details['description']

    ## Dependencies
    dependencies = ""
    if cmd in schema["$defs"]["protocol"]['dependentRequired']:    
      dependencies += "**Dependencies:** "
      dependencies += ", ".join( [ f"`{x}`_" for x in schema["$defs"]["protocol"]['dependentRequired'][cmd]])

    ## Command example
    example = Template(EXAMPLE).substitute(
      code = cmd_example(details, schema, cmd)
    ).lstrip()

    ## Command configuration
    config = cmd_details_print( cmd_details(details, schema) )

    ## Populate the template
    cmd_content = Template(COMMAND).substitute(
      commandname= cmd,
      title_underline = "-" * len(cmd),
      description = description,
      example = example,
      config = config,
      dependencies = dependencies
    ).rstrip()

    ## Append section to command list
    rst_cmds.append(cmd_content)

  ## Build header content
  rst_content = Template(BODY).substitute(
    href = schema["$schema"],
    commands= "\n\n----\n\n".join(rst_cmds)
  )

  ## Generate path for documention file
  path = os.path.join( os.path.dirname(__file__), '..', 'protocol-schema.rst' )
  if os.path.exists( path ):
    os.remove( path )
    
  ## Write out file
  with open( os.path.join( os.path.dirname(__file__), '..', 'protocols-schema.rst' ), 'w+') as f:
      f.write(rst_content)

def cmd_details(details, schema, level=0):

  cmd_configs = []

  ## References
  if '$ref' in details:
    ref_key = details['$ref'][8:]
    if ref_key in schema['$defs']:
      details = {**details, **schema['$defs'][ref_key]}
      del details["$ref"]

  ## Type
  if 'type' in details:

    ## Count elements and remove items not displayed
    key_count = list(details.keys())
    if "pattern" in key_count:
      key_count.remove("pattern")
    key_count = len(key_count)

    item_msg = ""
    if 'minItems' in details or 'maxItems' in details:
      item_msg = " items_msg"

    if isinstance(details["type"], str):
      cmd_configs.append( "**%s**%s" % (details["type"].capitalize(), item_msg ) )
    if isinstance(details["type"], list):
      cmd_configs.append( "**%s** %s".capitalize() % (", ".join([x.capitalize() for x in details["type"]] ),item_msg) )

  ## Enum Values
  if 'enum' in details:
    cmd_configs.append( "*Values:* %s" % ", ".join( [str(x) for x in details["enum"]]) )

  ## Maxiumum Value
  if 'minimum' in details:
    cmd_configs.append( "*Minimum:* %s" % details["minimum"] )

  ## Maxiumum Value
  if 'maximum' in details:
    cmd_configs.append( "*Maximum:* %s" % details["maximum"] )

  ## Min/Max Array Elements (Items)
  item_count_msg = None
  if 'minItems' in details and 'maxItems' in details:
    if details["minItems"] == details["maxItems"]:
      item_count_msg = "(Exactly %s item%s)" % (details["maxItems"], "s" if details["maxItems"] > 1 else "" )
    else:
      item_count_msg = "(Between %s and %s items)" % (details["minItems"],details["maxItems"])

  elif 'minItems' in details:
    item_count_msg = "(At least %s item%s)" % (details["maxItems"], "s" if details["maxItems"] > 1 else "" )

  elif 'maxItems' in details:
    item_count_msg = "(Up to %s item%s)" % (details["maxItems"], "s" if details["maxItems"] > 1 else "" )

  ## Replace items_msg tag with min/max message
  if not item_count_msg is None:
    for idx,n in enumerate(cmd_configs):
      if isinstance(n, str):
        cmd_configs[idx] = n.replace("items_msg", item_count_msg)

  ## Prefix Items
  if 'prefixItems' in details:
    prefixItems = ["*Order and type for first %s item%s (Required)*" % ( len(details['prefixItems']) , "s" if len(details['prefixItems']) > 1 else "" )]
    for prefixItem in details['prefixItems']:
      if isinstance(prefixItem, dict):
        prefixItems.append( cmd_details( prefixItem, schema, level+1) )

    cmd_configs += prefixItems

  ## Items
  if 'items' in details:
    items_out = []

    if isinstance(details['items'], dict):
      items_out.append(cmd_details( details['items'], schema, level+1))
    
    if isinstance(details['items'], list):
      for item in details['items']:
        if isinstance(item, dict):
          items_out.append( cmd_details( item, schema, level+1) )

    cmd_configs += items_out

  ## oneOf, anyOf, allOf logic
  if any( x in details for x in ['anyOf','oneOf', 'allOf']):
    key = None
    if 'oneOf' in details:
      of_out = ["Only ``One`` of the following"]
      key = 'oneOf'
    if 'anyOf' in details:
      of_out = ["``Any`` of the following"]
      key = 'anyOf'
    if 'allOf' in details:
      of_out = ["``**All**`` of the following"]
      key = 'allOf'

    for idx, Of in enumerate(details[key]):
      of_out.append(cmd_details( Of, schema, level+1))

    cmd_configs += of_out

  ## Descriptions
  if 'description' in details and level > 0:
    cmd_configs.append( "*%s*" % details["description"] )

  return cmd_configs

def cmd_details_print(details, level=0):

  ## Output string
  out = ""

  ## For Testing
  if level == 0 and DEV:
    out = json.dumps(details) + '\n\n\n.. rst-class:: inline-style-none\n\n\n'
  
  for detail in details:

    if isinstance(detail, str):
      out += "%s- %s\n" % (("  " * level), detail)
    
    ## increase level by one if we encounter a list
    if isinstance(detail, list):
      out += "\n" + cmd_details_print(detail, level+1)

  return out

def cmd_example(details, schema, cmd):

  ## References
  if '$ref' in details:
    ref_key = details['$ref'][8:]
    if ref_key in schema['$defs']:
      details = {**details, **schema['$defs'][ref_key]}
      del details["$ref"]

  ## Examples
  example = ""
  if 'examples' in details:
    ## Show example
    for idx, item in enumerate(details['examples']):

      if len(details['examples']) == 1:
        example += "## Code Example\n"
      else:
        example += "%s## Code Example #%s\n" % (( "\n" if idx > 0 else "" ), (idx+1))

      if 'type' in details and  details['type'] == "string" :
        example += "%s: \"%s\"\n" % (cmd, item)
      else:
        example += "%s: %s\n" % (cmd, json.dumps(item, indent=2) )

  else:
    example = "## Code Example\n%s: <input>" % cmd

  example = "\n".join(["  " + str(x) for x in example.split("\n")])

  return example
