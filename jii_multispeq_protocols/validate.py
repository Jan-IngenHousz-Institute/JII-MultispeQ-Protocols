"""
Test your protocol for issues before you continue
to work with it or you publish it.
"""

import json
import jsonschema
import os
import warnings
from typing import Dict, List, Tuple

def validate ( protocol=None, verbose=False ):
  """
  Test protocol

  :param protocol: Protocol code to test
  :param type: dict or str
  :param verbose: Print errors
  :param type: bool

  :return: True if tests are passed with an empty list, otherwise False with a list of errors
  :rtype: bool, list
  """

  file_path = os.path.join(os.path.dirname(__file__), 'schema.json' )

  try:
    with open( file_path, 'r', encoding='utf-8') as fp:
      schema = json.load( fp )
  except json.JSONDecodeError:
    warnings.warn('Error: Invalid JSON (%s)' % file_path )
    schema = {}
    pass

  validator = SchemaValidator(schema)
  
  is_valid, errors = validator.validate_with_all_errors(protocol)
  if not is_valid and verbose:
      for error in errors:
          print(error)

  return is_valid, errors


class SchemaValidator:
    def __init__(self, schema: Dict):
        self.schema = schema
        self.validator = jsonschema.Draft202012Validator(schema)

    def validate_with_all_errors(self, data: Dict) -> Tuple[bool, List[str]]:
        """
        Validates data and returns all validation errors.
        
        Args:
            data: The data to validate against the schema
            
        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        errors = []
        try:
            for error in self.validator.iter_errors(data):
                # Format error path
                path = ' -> '.join(str(p) for p in error.path) if error.path else 'root'
                # Create detailed error message
                error_msg = f"Path '{path}': {error.message}"
                errors.append(error_msg)
        except AttributeError:
           pass
        
        return len(errors) == 0, errors