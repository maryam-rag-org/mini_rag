from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def welcome_message():
    return {"message": "Welcome to the Mini RAG App!"}