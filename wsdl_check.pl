import os
import sys
import json
from suds.client import Client
import schema_conv

def parse_operations(services):
  for service in services:
    for port in service.ports:
      print(port.binding.operations)
      for operation in port.binding.operations:
        print(operation)
        for part in port.binding.operations[operation].soap.input.body.parts:
          print('< ' + part.name + ':' + part.type[0])
        for part in port.binding.operations[operation].soap.output.body.parts:
          print('> ' + part.name + ':' + part.type[0])


if __name__ == "__main__":
  #url = 'https://payzen.lyra-labs.fr/vads-ws/v4?wsdl'
  url = 'file://' + os.getcwd() + '/' + sys.argv[1]
  client = Client(url)


  schema = schema_conv.parse_xsd_schema(client.wsdl.schema)
  #print(schema)
  #print(json.dumps(schema, sort_keys=False, indent=2))
  #parse_operations(client.wsdl.services)
