import os
import sys
import re
import json
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from suds.client import Client
import schema_conv
import services
from jinja2 import Environment, FileSystemLoader

schema = {}
endpoints = {}
jinja_env = None

def render_json(request, element):
  response = Response(json.dumps(element, sort_keys=False, indent=2))
  response.content_type = 'application/json; charset=utf-8'
  return response

def render_template(template_name, path, **context):
  p = context['path'] = []
  fp = ''
  for entry in path:
    fp = fp + '/' + entry
    p.append( { 'fullpath': fp, 'entry': entry} )
  p.insert(0, { 'fullpath': '/', 'entry': 'API Root' } )
  template = jinja_env.get_template(template_name)
  print(context)
  response = Response(template.render(context))
  response.content_type = 'text/html; charset=utf-8'
  return response

def view_root(request):
  return render_template('root.html', [])

def view_message(request, message):
  try:
    message_schema = schema[message]
  except KeyError:
    return NotFound()
  return render_json(request, message_schema)

def edit_message(request, message):
  try:
    message_schema = schema[message]
  except KeyError:
    return NotFound()
  return render_json(request, message_schema)

def view_messages_list(request):
  return render_html(request, list(schema.keys()))

def view(request, element, path):
  return render_json(request, element)

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
    elif len(path) >= 1 and path[0] == 'messages':
      if len(path) == 1:
        return view_messages_list(request)
      elif len(path) == 2:
        return view_message(request, path[1])
      elif len(path) == 3 and path[2] == 'editor':
        return edit_message(request, path[1])
      else:
        return NotFound()
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
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
    # jinja_env.filters['hostname'] = get_hostname
    client = Client(url)
    schema = schema_conv.parse_xsd_schema(client.wsdl)
    endpoints = services.parse_services(client.wsdl)
    run_simple('localhost', 4000, application)
  else:
    print('Usage: ' + sys.argv[0] + ' <wsdl path or url>')
