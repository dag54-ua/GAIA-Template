from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routers.incidents import router as incidents_router

app = FastAPI(title="Neighborhood Association API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5188"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-User-Id"],
)

app.include_router(incidents_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
