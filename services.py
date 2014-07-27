import schema_conv

def add_io(operation, part):
  type_name = part.type[0]
  type_desc = None
  try:
    base_type = schema_conv.xsd_to_json_type(type_name)
  except KeyError:
    base_type = None

  io = { 'name':part.name }
  if base_type is not None:
    io['type'] = { 'type':type_name, 'js:type':base_type, 'xs:type':type_name }
  else:
    io['type'] = { 'type':type_name, 'js:type':'object', 'xs:type':'element' }
    # HAL will do the job
    io['_links'] = { 'schema':{'href':'schemas/' + type_name} }

  operation.append(io)

def parse_services(services):
  endpoints = {}
  for service in services:
    srv = endpoints[service.name] = {}
    for port in service.ports:
      prt = srv[port.name] = {}
      for operation in port.binding.operations:
        ope = prt[operation] = { 'input':[], 'output':[] }
        for part in port.binding.operations[operation].soap.input.body.parts:
          add_io(ope['input'], part)
        for part in port.binding.operations[operation].soap.output.body.parts:
          add_io(ope['output'], part)
  return endpoints
