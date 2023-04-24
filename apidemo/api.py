from ninja import NinjaAPI, Schema
from datetime import date
from typing import List
from django.shortcuts import get_object_or_404
from pets.models import Pet

api = NinjaAPI()

class PetIn(Schema):
    name: str
    species: str = None
    age: int = None

class PetOut(Schema):
    id: int
    name: str
    species: str
    age: int

@api.get('/pets/{pet_id}', response=PetOut)
def get_pet(request, pet_id: int):
    pet = Pet.objects.get(id=pet_id)
    return pet

@api.get('/pets/', response=List[PetOut])
def get_pets(request):
    pets = Pet.objects.all()
    return pets

@api.post('/pets/')
def create_pet(request, payload: PetIn):
    new_pet = Pet.objects.create(**payload.dict())
    return {'id': new_pet.id}

@api.put('/pets/{pet_id}')
def update_pet(request, pet_id: int, payload: PetIn):
    pet = get_object_or_404(Pet, id=pet_id)
    for attr, value in payload.dict().items():
        if value != None:
            setattr(pet, attr, value)
    pet.save()
    return { 'success': True }

@api.delete('/pets/{pet_id}')
def delete_pet(request, pet_id: int):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return {'success': True}

# @api.get('/employees/{employee_id}', response=EmployeeOut)
# def get_employee(request, employee_id: int):
#     employee = get_object_or_404(Employee, id=employee_id)
#     return employee

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
