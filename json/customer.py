from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal

from flask_openapi3 import Tag, APIView
from pydantic import BaseModel, Field

customer_tag = Tag(name="Customer")

api = APIView(url_prefix="/api/v1")


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


class CustomerGet(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_customer(customer: Customer) -> CustomerGet:
        return CustomerGet(id=customer.id, name=customer.name)


class CustomerPut(BaseModel):
    name: str

class CustomerPost(CustomerPut):
    pass

class CustomerGetList(BaseModel):
    data: List[CustomerGet]


class EntityPath(BaseModel):
    id: int = Field(..., description="Entity id")


class EntityQuery(BaseModel):
    order_by: Literal['ASC', 'DESC']


@api.route("/customer/{id}")
class CustomerResource:
    @api.doc(summary="Get customer", tags=[customer_tag], responses={200: CustomerGet})
    def get(self, path: EntityPath):
        obj = customer_repo.get_by_id(path.id)
        return CustomerGet.from_customer(obj).model_dump(mode='json')

    @api.doc(summary="Delete customer", tags=[customer_tag], responses={200: CustomerGet})
    def delete(self, path: EntityPath):
        obj = customer_repo.get_by_id(path.id)
        customer_repo.delete(path.id)
        return CustomerGet.from_customer(obj).model_dump(mode='json')

    @api.doc(summary="Update customer", tags=[customer_tag], responses={200: CustomerGet})
    def put(self, path: EntityPath, body: CustomerPut):
        obj = customer_repo.update(customer_id=path.id, customer={"name": body.name})
        return CustomerGet.from_customer(obj).model_dump(mode='json')


@api.route("/customers")
class CustomerList:
    @api.doc(summary="Get customer list", tags=[customer_tag], responses={200: CustomerGetList})
    def get(self, query: EntityQuery):
        objs = customer_repo.get_all(order_by=query.order_by)
        return {"data": [CustomerGet.from_customer(o).model_dump(mode='json') for o in objs]}

    @api.doc(summary="Create customer", tags=[customer_tag], responses={200: CustomerGet})
    def post(self, body: CustomerPost):
        raw_customers = customer_repo.get_all()
        if len(raw_customers) > 0:
            next_id = max([o.id for o in raw_customers]) + 1
        else:
            next_id = 0
        customer_repo.store({"id": next_id, "name": body.name})
        customer = customer_repo.get_by_id(next_id)
        return CustomerGet.from_customer(customer).model_dump(mode='json')


customer_repo = CustomerRepository()
