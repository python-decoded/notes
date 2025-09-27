import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import books
from core.handlers import add_handlers


app = FastAPI()
add_handlers(app)


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
