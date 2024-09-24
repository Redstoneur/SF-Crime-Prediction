from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str


class MyAPI(FastAPI):
    def __init__(self):
        super().__init__()
        self.add_routes()

    def add_routes(self):
        @self.get("/")
        def read_root():
            return {"message": "Hello, World!"}

        @self.get("/hello/{name}")
        def say_hello(name: str):
            return {"message": f"Hello, {name}!"}

        @self.post("/welcome")
        def welcome_user(user: User):
            return {"message": f"Welcome, {user.name}!"}


# Assurez-vous que l'objet `app` est déclaré ici
app = MyAPI()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
