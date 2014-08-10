import os
import sys
import json
from suds.client import Client
import schema_conv
from jsonschema import validate

if __name__ == "__main__":
  if len(sys.argv) == 2:
    if sys.argv[1].find('http') == 0:
      url = sys.argv[1]
    else:
      url = 'file://' + os.getcwd() + '/' + sys.argv[1]
    client = Client(url)
    schema = schema_conv.parse_xsd_schema(client.wsdl)
    print(json.dumps(schema, sort_keys=False, indent=2))
    # print(schema)
    # data = {'deliverySpeed':'b'}
    # validate( data, schema )
  else:
    print('Usage: ' + sys.argv[0] + ' <wsdl path or url>')
