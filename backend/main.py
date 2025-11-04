from fastapi import FastAPI


app = FastAPI(title="air_quality backend")

@app.get("/")
def read_root():
    return {"status": "ok"}
