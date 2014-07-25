import os
import sys
import json
from suds.client import Client

#url = 'https://payzen.lyra-labs.fr/vads-ws/v4?wsdl'
#url = 'file://' + os.getcwd() + '/v4.wsdl'
url = 'file://' + os.getcwd() + '/' + sys.argv[1]

client = Client(url)

def xsd_to_json_type(name):
  mapping = {
    'string': 'string',
    'int': 'integer',
    'long': 'integer',
    'boolean': 'boolean',
    'dateTime': 'integer',
    'null': None
  }
  return mapping[name]

def parse_xsd_complex_type(document, element):
  document['$schema'] = 'http://json-schema.org/draft-04/schema#'
  document['title'] = element.name
  document['type'] = 'object'
  document['description'] = 'ComplexType ' + element.name + ' generated from XSD'
  p = document['properties'] = {}
  r = None

  for seqel in element.children():
    e = seqel[0]
    q = p[e.name] = {}

    if e.min is None:
      if r is None:
        r = document['required'] = []
      r.append(e.name)
    elif e.max is not None:
      q = p[e.name] = { 'type': 'array', 'items': {} }
      q = q['items']

    if e.type is not None:
      try:
        baseType = xsd_to_json_type(e.type[0])
        q['type'] = baseType
        q['description'] = e.name + ': XSD type ' + e.type[0]
      except KeyError:
        q['$ref'] = '#/properties/' + e.type[0]
    else:
      # print('### embedded-type:' + e.root.name)
      parse_xsd_complex_type(q, e)


def parse_xsd_simple_type(document, element):
  # document['title'] = element.name
  # document['description'] = 'SimpleType ' + element.name + ' generated from XSD'
  pass


def parse_xsd_schema(schema):
  root = { 'id':'#root' }
  elements = root['properties'] = {}
  for schel in client.wsdl.schema.children:
    element_name = schel.name
    element_type = schel.root.name
    document = { 'id': '#' + element_name }
    if element_type == "complexType":
      parse_xsd_complex_type(document, schel)
    elif element_type == "simpleType":
      parse_xsd_simple_type(document, schel)
    else:
      raise Exception('Unsupported Schema definition: ' + element_type)
    elements[element_name] = document
  return root

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


#parse_operations(client)
schema = parse_xsd_schema(client.wsdl.schema)
print(json.dumps(schema, sort_keys=False, indent=2))
