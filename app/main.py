from fastapi import FastAPI

app = FastAPI(title="AI Job Assistant")

@app.get("/")
def root():
    return {"message": "First try."}
