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

def view(request, element, path):
  return Response(json.dumps(element, sort_keys=False, indent=2))

def browse(request, parent, path, index):
  if len(path) == index:
    return view(request, parent, path)
  else:
    try:
      children = parent[path[index]]
    except KeyError:
      return NotFound()
    return browse(request, children, path, index + 1)

@Request.application
def application(request):
  if request.method == 'GET':
    #return browse_root(request)
    path = list(filter((lambda x: len(x) > 0), re.split('/+', request.path)))
    return browse(request, endpoints, path, 0)
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
