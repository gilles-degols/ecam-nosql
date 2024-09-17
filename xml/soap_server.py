import logging
from dataclasses import dataclass
from typing import List

from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, Array, ComplexModel, UnsignedInteger32
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.protocol.xml import XmlDocument
from spyne.server.wsgi import WsgiApplication

logging.basicConfig(level=logging.DEBUG)


@dataclass
class CustomerSchema(ComplexModel):
    id: int = UnsignedInteger32(pk=True)
    name: str = Unicode(150, min_len=4, pattern='[a-z0-9.]+')


@dataclass(frozen=False)
class Customer:
    id: int
    name: str


class CustomerRepository:
    def __init__(self):
        self._customers = []
        for i in range(0, 50):
            self._customers.append(Customer(i, f"Name {i}"))

    def get_all(self, order_by: str = "ASC") -> List[Customer]:
        customers = sorted(self._customers, key=lambda k: k.name, reverse=order_by != "ASC")
        return customers

    def get_by_id(self, customer_id: int) -> Customer:
        return next((c for c in self._customers if c.id == customer_id))

    def store(self, customer: dict) -> Customer:
        self._customers.append(Customer(**customer))
        return self._customers[-1]

    def update(self, customer_id: int, customer: dict) -> Customer:
        current_customer = self.get_by_id(customer_id)
        for k, v in customer.items():
            setattr(current_customer, k, v)
        return current_customer

    def delete(self, customer_id: int) -> bool:
        target = None
        for i, c in enumerate(self._customers):
            if c.id == customer_id:
                target = i
        if target is not None:
            del self._customers[target]
        return True


class CustomerController(ServiceBase):

    @rpc(Unicode(values=["ASC", "DESC"]), _returns=Array(CustomerSchema))
    def customer_get_list(ctx, order_by="ASC"):
        items = customer_repo.get_all(order_by)
        return items

    @rpc(Unicode, _returns=CustomerSchema)
    def customer_get(ctx, customer_id):
        customer = customer_repo.get_by_id(int(customer_id))
        return customer

    @rpc(Unicode(), _returns=CustomerSchema)
    def customer_create(ctx, name):
        """Docstrings for create customer   in the wsdl.

            @param name the customer name

            @return the completed Customer Object
         """

        if len(customer_repo._customers) > 0:
            id = max(*[c.id for c in customer_repo._customers]) + 1
        else:
            id = 0

        payload = {
            "id": id,
            "name": name,
        }
        customer = customer_repo.store(payload)
        return customer

    @rpc(Unicode(), Unicode(), _returns=CustomerSchema)
    def customer_edit(ctx, customer_id, name):
        """Docstrings for create customer   in the wsdl.

            @param customer_id the customer id
            @param name the customer name
            @param family the customer family
            @param address the customer address

            @return the completed Customer Object
         """

        payload = {
            "name": name
        }

        customer = customer_repo.update(customer_id, payload)

        return customer

    @rpc(Unicode(), _returns=CustomerSchema)
    def customer_delete(ctx, customer_id):
        """Docstrings for create customer   in the wsdl.

            @param customer_id the customer id
            @return the completed Customer Object
         """

        customer = customer_repo.delete(customer_id)

        return customer


customer_repo = CustomerRepository()
application = Application([CustomerController],
                          tns='python.soap.example',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
