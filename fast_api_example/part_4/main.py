import json
from typing import Annotated
from fastapi import (FastAPI, Request, Path, Query, Header, Cookie, Body,
                     Response, Form, File, UploadFile, Depends, Security)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from routers import books
from core.handlers import add_handlers
from contextlib import asynccontextmanager
from core.db import init_db, drop_db, AsyncSessionLocal


@asynccontextmanager
async def app_setup(app: FastAPI):
    async with AsyncSessionLocal() as session:
        await init_db(session)

    yield

    await drop_db()


app = FastAPI(lifespan=app_setup)
add_handlers(app)


async def get_user(
        user_creds: Annotated[HTTPBasicCredentials, Security(HTTPBasic())],
        res: Response
) -> dict:
    # Під'єднатись до бази даних і створити конекшн
    res.headers["DI-HEADER"] = "Hi!!!!!"
    yield {"user_name": user_creds.username,
           "password": user_creds.password,
           "user_age": 27}
    # Закрити конекшн після обробки запиту


@app.get("/echo/{something}")
async def echo(req: Request,
               user: Annotated[dict, Depends(get_user)],
               res: Response,
               param1: Annotated[str, Form()],
               content_type: Annotated[str, Header()],
               something: Annotated[str, Path(max_length=4)],
               authorization: Annotated[str, Header()] = None,
               req_body: Annotated[str, Body()] = None,
               param2: Annotated[str, Form()] = None,
               image: Annotated[UploadFile, File()] = None,
               session_id: Annotated[str, Cookie()] = None,
               foo: Annotated[int, Query(lt=100)] = 1):

    res.headers["MAIN-HEADER"] = "Hi!!!!!"

    url = req.url
    path_params = {"something": something}
    query_params = {"foo": foo}
    method = req.method
    headers = req.headers
    body = await req.form()
    body = {k: v for k, v in body.items()
            if not isinstance(v, UploadFile)}

    return {"url": url, "path_params": path_params,
            "query_params": query_params, "method": method,
            "headers": headers, "body": body, "file": image and image.filename,
            "user": user, "auth": authorization}


@app.middleware("http")
async def response_formatter(req: Request, call_next):
    # Щось зробити перед обробкою запиту

    response = await call_next(req)

    # Щось зробити після обробки запиту
    if response.headers.get("content-type") != "application/json":
        return response

    raw_body = b"".join([chunk async for chunk in response.body_iterator])
    content = json.loads(raw_body.decode())
    if "detail" not in content:
        content = {"detail": content}
    content["middleware_was_here"] = True

    return JSONResponse(status_code=response.status_code,
                        content=content)


@app.get("/status")
async def status():
    return {"status": "running"}


app.include_router(books.router, prefix="/books")
