import os
from suds.client import Client

#url = 'https://payzen.lyra-labs.fr/vads-ws/v4?wsdl'
url = 'file://' + os.getcwd() + '/v4.wsdl'

client = Client(url)

for ctype in client.wsdl.schema.children:
  print(ctype.name)
  for seq in ctype.root.children:
    for el in seq.children:
      print(el)
      print(el.__dict__)

for service in client.wsdl.services:
  for port in service.ports:
    #print(port.binding.operations)
    for operation in port.binding.operations:
      print(operation)
      for part in port.binding.operations[operation].soap.input.body.parts:
        print('< ' + part.name + ':' + part.type[0])
      for part in port.binding.operations[operation].soap.output.body.parts:
        print('> ' + part.name + ':' + part.type[0])

#print(client.factory.resolver.schema.__dict__)
#print(client.wsdl.schema.__dict__)

#print(dir(client.items))
#print("=================")
#print(dir(client))
#print("=================")
#print(dir(client.service))
#print("=================")
#print(dir(client.service[0]))

#print(client.service[0]._MethodSelector__methods.keys())
#print(list(client.service[0]._MethodSelector__methods.keys()))
#print(client.service[0]._MethodSelector__methods['create'].soap.input)
#print(client.service[0]._MethodSelector__methods['create'].soap.input.body)
#print(client.service[0]._MethodSelector__methods['create'].soap.input.body.parts)
#print("=================")
#print(client.service[0]._MethodSelector__methods['create'].soap.input.body.parts[0])
#print("=================")
#for i in (client.service[0]._MethodSelector__methods['create'].soap.input.body.parts):
#  print(i.name + ',' + i.type[0])
