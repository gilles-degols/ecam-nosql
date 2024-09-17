from zeep import Client

client = Client(wsdl='http://localhost:8000/?wsdl')
result = client.service.customer_get(1)
print(result)