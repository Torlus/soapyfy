import schema_conv


def add_io(operation, part):
    type_name = part.type[0]
    type_desc = None
    try:
        base_type = schema_conv.xsd_to_json_type(type_name)
    except KeyError:
        base_type = None

    io = {'name': part.name}
    if base_type is not None:
        io['type'] = {'type': type_name, 'js:type': base_type, 'xs:type': type_name}
    else:
        io['type'] = {'type': type_name, 'js:type': 'object', 'xs:type': 'element'}
        # HAL will do the job
        io['_links'] = {'schema': {'href': 'schema/#/properties/' + type_name}}

    operation.append(io)


def add_io_msg(io_msg):
    name = 'message_' + io_msg.name
    return {
        'type': name,
        '_links': {
            'schema': {'href': 'schema/#/properties/' + name},
            'validate': {'href': 'schema/#/properties/' + name, 'method': 'post'}
        }
    }


def parse_services(wsdl):
    endpoints = {}
    input_msgs = {}
    output_msgs = {}
    # print(dict(wsdl))
    # print(dict(wsdl.bindings))
    bindings = list(wsdl.bindings.values())
    for binding in bindings:
        # print(binding.type.operations)
        for operation in binding.type.operations:
            inp_msg = binding.type.operations[operation].input
            input_msgs[operation] = add_io_msg(inp_msg)
            out_msg = binding.type.operations[operation].output
            output_msgs[operation] = add_io_msg(out_msg)

    for service in wsdl.services:
        srv = endpoints[service.name] = {}
        for port in service.ports:
            prt = srv[port.name] = {}
            # print(port.binding.operations)
            for operation in port.binding.operations:
                ope = prt[operation] = {'input': {}, 'output': {}}
                ope['input'] = input_msgs[operation]
                ope['output'] = output_msgs[operation]
                # print(port.binding.operations[operation])
                # ope = prt[operation] = { 'input':[], 'output':[] }
                # for part in port.binding.operations[operation].soap.input.body.parts:
                # add_io(ope['input'], part)
                # for part in port.binding.operations[operation].soap.output.body.parts:
                #   add_io(ope['output'], part)
    return endpoints
