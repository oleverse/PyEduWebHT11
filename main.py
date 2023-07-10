from fastapi import FastAPI

from api.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Welcome to PyWebEduHT11!"}
