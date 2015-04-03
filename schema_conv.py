import copy
from suds.xsd.sxbasic import Simple, Complex, Element, Restriction

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
            q = p[e.name] = {'type': 'array', 'items': {}}
            q = q['items']

        if e.type is not None:
            try:
                base_type = xsd_to_json_type(e.type[0])
                q['type'] = base_type
                q['description'] = e.name + ': XSD type ' + e.type[0]
            except KeyError:
                q['$ref'] = '#/definitions/' + e.type[0]
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


def parse_wsdl_message_parts(document, parts):
    p = document['properties'] = {}
    r = document['required'] = []
    for part in parts:
        part_name = part.name
        r.append(part_name)
        q = p[part_name] = {}

        if part.element is None:
            try:
                base_type = xsd_to_json_type(part.type[0])
                q['type'] = base_type
                q['description'] = part_name + ': XSD type ' + part.type[0]
            except KeyError:
                q['$ref'] = '#/definitions/' + part.type[0]
        else:
            q['$ref'] = '#/definitions/' + part.element[0]

    return document


def parse_xsd_schema(wsdl):
    messages = {}

    root = {'id': '#root'}
    root['$schema'] = json_schema_version
    root['type'] = 'object'

    elements = root['definitions'] = {}
    for schel in wsdl.schema.children:
        element_name = schel.name
        document = {'id': '#' + element_name}
        if isinstance(schel, Complex):
            parse_xsd_complex_type(document, schel)
        elif isinstance(schel, Simple):
            parse_xsd_simple_type(document, schel)
        elif isinstance(schel, Element):
            pass
        else:
            raise Exception('Unsupported Schema definition: ' + schel.str())
        elements[element_name] = document

    for msgel in wsdl.messages:
        message_name = 'message_' + msgel[0]

        document = copy.copy(root)
        document['id'] = '#' + message_name
        document['$schema'] = json_schema_version
        document['title'] = message_name
        document['description'] = message_name

        parse_wsdl_message_parts(document, wsdl.messages[msgel].parts)

        messages[message_name] = document
    return messages
