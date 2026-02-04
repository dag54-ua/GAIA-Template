from fastapi import FastAPI

app = FastAPI(title="Neighborhood Association API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
