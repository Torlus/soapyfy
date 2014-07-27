from suds.xsd.sxbasic import Simple, Complex, Restriction

json_schema_version = 'http://json-schema.org/draft-04/schema#'

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
  document['$schema'] = json_schema_version
  document['title'] = element.name
  document['description'] = 'ComplexType ' + element.name + ' generated from XSD'
  document['type'] = 'object'

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
      if isinstance(e.rawchildren[0], Complex):
        parse_xsd_complex_type(q, e)
      else:
        raise Exception('Unsupported Schema definition: ' + e.rawchilden[0].str())

def parse_xsd_simple_type(document, element):
  document['$schema'] = json_schema_version
  document['title'] = element.name
  document['description'] = 'SimpleType ' + element.name + ' generated from XSD'

  ev = None

  if isinstance(element.rawchildren[0], Restriction):
    try:
      document['type'] = element.rawchildren[0].ref[0]
    except:
      pass
    for val in element.children():
      if ev is None:
        ev = document['enum'] = []
      ev.append(val[0].name)
  else:
    raise Exception('Unsupported Schema definition: ' + element.rawchilden[0].str())

def parse_xsd_schema(schema):
  root = { 'id':'#root' }
  elements = root['properties'] = {}
  for schel in schema.children:
    element_name = schel.name
    document = { 'id': '#' + element_name }
    if isinstance(schel, Complex):
      parse_xsd_complex_type(document, schel)
    elif isinstance(schel, Simple):
      parse_xsd_simple_type(document, schel)
    else:
      raise Exception('Unsupported Schema definition: ' + schel.str())
    elements[element_name] = document
  return root
