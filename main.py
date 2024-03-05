from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware



from pydantic import BaseModel, Field, EmailStr


origins = [
    "https://70.139.132.129",
    "https://avashist.com",
    "https://events-app.avashist.com",
    "https://avashist1998.github.io",
]



users = APIRouter()


class UserInfo(BaseModel):
    """User Base model"""
    name: str = Field(immutable=False)
    email: EmailStr = Field(immutable=True)


@users.get("/", response_model=UserInfo)
async def get_user():
    """Get user info"""
    return UserInfo(name="user", email="user@email.com")


@users.post("/", response_model=UserInfo)
async def post_user(user: UserInfo, response: Response):
    """Get user info"""
    response.set_cookie(
        key="Auth",
        # domain=request.app.config.DOMAIN,
        value="289irjf928j9f",
        secure=True,
        samesite="none",
        httponly=True,
        max_age=3600,
    )
    return user


@users.post("test/", response_model=UserInfo)
async def test_user(user: UserInfo, request: Request):
    session_id = request.cookies.get("Auth")
    print(session_id)
    if not session_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"Session id": session_id}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(users, tags=["users"], prefix="/users")


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        log_level="info",
        # ssl_keyfile="",
        # ssl_certfile="",
    )