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
root = {}

def render(request, element, path):
  response = Response(json.dumps(element, sort_keys=False, indent=2))
  response.content_type = 'application/json; charset=utf-8'
  return response

def view_root(request):
  return render(request, root, [])

def view_schema(request, message):
  try:
    message_schema = schema[message]
  except KeyError:
    return NotFound()
  return render(request, message_schema, [])

def view_schema_list(request):
  return render(request, list(schema.keys()), [])

def view(request, element, path):
  return render(request, element, path)

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
    path = list(filter((lambda x: len(x) > 0), re.split('/+', request.path)))
    if len(path) == 0:
      return view_root(request)
    elif len(path) >= 2 and path[0] == 'messages':
      return view_messages(request, path[1])
    elif len(path) >= 1 and path[0] == 'messages':
      return view_messages_list(request)
    elif len(path) >= 1 and path[0] == 'services':
      return browse(request, endpoints, path, 1)
    else:
      return NotFound()
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
    schema = schema_conv.parse_xsd_schema(client.wsdl)
    endpoints = services.parse_services(client.wsdl)
    root = { }
    run_simple('localhost', 4000, application)
  else:
    print('Usage: ' + sys.argv[0] + ' <wsdl path or url>')
