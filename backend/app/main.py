from fastapi import FastAPI

from app.presentation.routers.incidents import router as incidents_router

app = FastAPI(title="Neighborhood Association API")
app.include_router(incidents_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
