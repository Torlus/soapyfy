import os
import sys
import json
from suds.client import Client
import schema_conv
import services

if __name__ == "__main__":
  if len(sys.argv) == 2:
    if sys.argv[1].find('http') == 0:
      url = sys.argv[1]
    else:
      url = 'file://' + os.getcwd() + '/' + sys.argv[1]
    client = Client(url)
    schema = schema_conv.parse_xsd_schema(client.wsdl.schema)
    print(json.dumps(schema, sort_keys=False, indent=2))
    endpoints = services.parse_services(client.wsdl.services)
    print(json.dumps(endpoints, sort_keys=False, indent=2))
  else:
    print('Usage: ' + sys.argv[0] + ' <wsdl path or url>')
