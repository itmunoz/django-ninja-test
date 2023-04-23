from ninja import NinjaAPI, Schema
from datetime import date
from typing import List
from django.shortcuts import get_object_or_404

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = 'world'

class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get('/me', response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {'message': 'Please sign in first'}
    return request.user

@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}

@api.post('/hello')
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"

# CRUD Endpoints

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    deparment_id: int = None
    birthdate: date = None

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    deparment_id: int = None
    birthdate: date = None

@api.post('/employees')
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {id: employee.id}

@api.get('/employees/{employee_id}', response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee

@api.get('/employees', response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs

@api.put('/employees/{employee_id}')
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {'success': True}

@api.delete('/employees/{employee_id}')
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {'success': True}

@api.get("/items/{item_id}")
def read_item(request, item_id: int):
    return {"item_id": item_id}
