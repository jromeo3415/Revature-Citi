'''
Day 4 - FastAPI application entrypoint

Day 7 update - Added CORS configuration to connect with frontend
'''

import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from app.routers import robots, missions, auth

load_dotenv()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

app = FastAPI(
    title="RoboPulse Fleet Command Center",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.2.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware, 

    # Endpoint for our frontend
    allow_origins=[FRONTEND_ORIGIN],

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

@app.get("/version", tags=["health"])
async def version() -> dict[str, str]:
    return {"version": app.version}



# BEGIN EXCEPTIONS


''' This exception handles when our database constraint (battery level not being
in range)
'''
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "A database constraint was violated (e.g. a duplicate value)."},
    )

# this is a catch-all exception handler so any unexpected failure returns a 
# constant JSON response
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error has occured."}
    )