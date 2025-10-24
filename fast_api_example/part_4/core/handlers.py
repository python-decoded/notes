from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from routers.books import ItemNotFoundException, AppBaseException


async def http_handler(req: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": exc.detail,
                                 "timestamp": datetime.now().isoformat(),
                                 "status": "failure"})


async def not_found_handler(req: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": exc.detail,
                                 "timestamp": datetime.now().isoformat(),
                                 "status": "failure"})


async def exception_handler(req: Request, exc: AppBaseException):
    print("exception_handler handler:", exc)
    status_code = 404 if isinstance(exc, ItemNotFoundException) else 500

    return JSONResponse(status_code=status_code,
                        content={"detail": f"{type(exc).__name__}: {str(exc)}",
                                 "timestamp": datetime.now().isoformat(),
                                 "status": "failure"})


def add_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_handler)
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(AppBaseException, exception_handler)
