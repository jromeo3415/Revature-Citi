'''
Day 4 - FastAPI application entrypoint
'''

from fastapi import FastAPI
from app.routers import robots, missions

app = FastAPI(
    title="RoboPulse Fleet Command Center",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.1.0"
)

app.include_router(robots.router)
app.include_router(missions.router )


# sample health endpoint to verify application is running correctly
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}