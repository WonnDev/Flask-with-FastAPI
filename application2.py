#(venv) --- uvicorn application2:app --reload
#uvicorn fastapi venv python-multipart
from types import NoneType
from fastapi import FastAPI, Path, Query, Form, Request, Response, Depends, Body, HTTPException,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Optional, List
import json, io
from uuid import UUID, uuid4
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.concurrency import iterate_in_threadpool
from pydantic import BaseModel
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(debug = True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

external_data = {}


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class UserModel(OurBaseModel):
	username: str | NoneType
	password: str | NoneType


class User(OurBaseModel):
	id : Optional[UUID] = uuid4()
	username: str | None
	password: str | None

db: List[User] = [
	User(
		id = uuid4(),
		username = "admin",
		password = "123"
		),
	User(
		id = uuid4(),
		username = "admin2",
		password = "123"
		)
]

class UpdateUser(BaseModel):
	username: str
	password: str

class Item(BaseModel):
	name: str
	price: float
	brand: str | None = None

class CreateItem(BaseModel):
	name: str
	price: float
	brand: str | None = None

class UpdateItem(BaseModel):
	name: str | None = None
	price: float | None = None
	brand: str | None = None

class UnicornException(Exception):
    def __init__(self, reponse: str):
        self.reponse = reponse


@app.get("/")
def home():
	return dict(external_data)

@app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(None, description = "The ID of item to view")):
def get_item(item_id: int | None):
	if item_id == 1:
		raise HTTPException(status_code=422, detail="Have userdata in data.")
	return external_data[item_id]

@app.get("/get-by-name")
# def get_item(name: str = Query(None, title = "Name", description = "Name of item")):
def get_item(name: str | None, description = "Name of item"):
	for item_id in external_data:
		if external_data[item_id].name == name:
			return external_data[item_id]
	return {"Data": "Not Found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
	if item_id in external_data:
		return {"Error" : "Item ID already exists"}
	external_data[item_id] = item
	return external_data[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
	if item_id not in external_data:
		return {"Error" : "Item ID not exists"}

	if item.name != None:
		external_data[item_id].name = item.name

	if item.price != None:
		external_data[item_id].price = item.price

	if item.brand != None:
		external_data[item_id].brand = item.brand

	return external_data[item_id]

@app.delete("/delete/")
# def delete_item(item_id: int = Query(..., description = "ID item Del")):
# 	if item_id not in external_data:
# 		return {"Error": "ID not found"}
# 	del external_data[item_id]
# 	return {"Success": "Item Deleted"}
async def delete(_id: UUID):
	for user in db:
		if user.id != _id:
			# return {"Error": "ID not found"}
			raise HTTPException(status_code=422, detail="ID not found!")
		db.remove(user)
		return {"Success": "Item Deleted"}

@app.post("/create-user/")
# def create_user(user_id: int, user : User): //{user_id} on endlink
# 	if user_id in external_data:
# 		return {"Error" : "User already exists"}
# 	external_data[user_id] = user
# 	return external_data[user_id]
async def create_user(user: User, request: Request):
	data: json = await request.body()
	data = data.replace(b"'", b'"')
	data = json.load(io.BytesIO(data))

	user.username = data['username']
	user.password = data['password']
	print(data)
	for usr in db:
		if data['username'] == usr.username:
			response = Response('User already exists! from Response', media_type='text/plain')
			# return {"detail" : "User already exists"}
			return response
			# raise HTTPException(status_code=422, detail="User already exists!")
	db.append(user)
	return db


@app.get("/api/get/users")
async def fetch_users(token: str = Depends(oauth2_scheme)):
	return {"token" : token}
	# return db (def clear)

@app.post("/api/auth/login")
async def login(username_login:str | None, password_login:str | None):
	# username_login = jsonable_encoder()
	# print(Request['username'])
	for user_id in external_data:
		if external_data[user_id].username == username_login and external_data[user_id].password == password_login:
			return {"Alert" : "Login Success!"}
		return {"Error" : "Username or password is incorect!"}
	return


@app.post("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
	if user_id not in external_data:
		return {"Error" : "User not exists"}

	if user.username != None:
		external_data[user_id].username = user.username

	if user.password != None:
		external_data[user_id].password = user.password

	return external_data[user_id]

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    print(response_body[0].decode())
    print(f"response_body={(b''.join(response_body)).decode()}")
    return response


   



		



