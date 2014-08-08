import os
import sys
import re
import json
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from suds.client import Client
import schema_conv
import services

schema = {}
endpoints = {}

def view_services(request, services):
  return Response(services)

def view_ports(request, ports):
  return Response(ports)

def browse_root(request):
  path = list(filter((lambda x: len(x) > 0), re.split('/+', request.path)))
  if len(path) == 0:
    return view_services(request, list(endpoints))
  else:
    try:
      service = endpoints[path[0]]
    except KeyError:
      return NotFound()
    return browse_service(request, service, path[1:])

def browse_service(request, service, path):
  if len(path) == 0:
    return view_ports(request, list(service))
  else:
    try:
      port = service[path[0]]
    except KeyError:
      return NotFound()
    return browse_port(request, port, path[1:])

def browse_port(request, port, path):
  return Response('operations=' + '|'.join(list(port)))

@Request.application
def application(request):
  if request.method == 'GET':
    return browse_root(request)
  elif request.method == 'POST':
    return Response('post')
  else:
    response = Reponse()
    response.status_code = 400
    return response

if __name__ == '__main__':
  from werkzeug.serving import run_simple
  if len(sys.argv) == 2:
    if sys.argv[1].find('http') == 0:
      url = sys.argv[1]
    else:
      url = 'file://' + os.getcwd() + '/' + sys.argv[1]
    client = Client(url)
    schema = schema_conv.parse_xsd_schema(client.wsdl.schema)
    endpoints = services.parse_services(client.wsdl.services)
    run_simple('localhost', 4000, application)
  else:
    print('Usage: ' + sys.argv[0] + ' <wsdl path or url>')
