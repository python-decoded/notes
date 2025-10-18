import json, uuid
from typing import Annotated
from starlette.datastructures import UploadFile as StarletteUploadFile
from fastapi import FastAPI, Request, Path, Query, Header, Cookie, Body, Form, File, UploadFile
from fastapi.responses import JSONResponse
from routers import books
from core.handlers import add_handlers


app = FastAPI()
add_handlers(app)





@app.get("/echo")
async def echo():
    return f"Message: {data}"













# @app.get("/echo/{something}")
# async def echo(req: Request,
#                req_body: Annotated[str, Body(None)],
#                param1: Annotated[str, Form(...)],
#                param2: Annotated[str, Form(None)],
#                image: Annotated[UploadFile, File(None)],
#                content_type: Annotated[str, Header("content-type")],
#                session_id: Annotated[str, Cookie(None)],
#                something: Annotated[str, Path(..., max_length=4)],
#                foo: Annotated[int, Query(1, lt=100)]):
#
#     url = req.url
#     path_params = {"something": something}
#     query_params = {"foo": foo}
#     # method = req.method
#     # headers = req.headers
#     # body = await req.form()
#     # file = body["image"]
#     # body = {k: v for k, v in body.items()
#     #         if not isinstance(v, UploadFile)}
#     #
#     # return {"url": url, "path_params": path_params,
#     #         "query_params": query_params, "method": method,
#     #         "headers": headers, "body": body, "file": file.filename}
#     #
#
#     return {"session_id": session_id, "contnet_type": content_type, "image": image}












# @app.middleware("http")
# async def response_formatter(req: Request, call_next):
#     # Щось зробити перед обробкою запиту
#
#     response = await call_next(req)
#
#     # Щось зробити після обробки запиту
#     if response.headers.get("content-type") != "application/json":
#         return response
#
#     raw_body = b"".join([chunk async for chunk in response.body_iterator])
#     content = json.loads(raw_body.decode())
#     if "detail" not in content:
#         content = {"detail": content}
#     content["middleware_was_here"] = True
#
#     return JSONResponse(status_code=response.status_code,
#                         content=content)


@app.get("/status")
async def status():
    return {"status": "running"}


app.include_router(books.router, prefix="/books")
