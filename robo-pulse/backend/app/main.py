'''
Day 4 - FastAPI application entrypoint

Day 7 update - Added CORS configuration to connect with frontend
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import robots, missions, auth

app = FastAPI(
    title="RoboPulse Fleet Command Center",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware, 

    # Endpoint for our frontend
    allow_origins=["http://localhost:5173", "http://192.168.1.248:5173", "http://100.68.190.75:5173/"],

    # this allows us to pass an authorization header using JWT
    allow_credentials=True,

    # this allows all methods and headers through
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(robots.router)
app.include_router(missions.router)
app.include_router(auth.router)

# sample health endpoint to verify application is running correctly
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}