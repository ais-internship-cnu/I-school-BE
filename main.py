from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Thank you hyoJeong"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
