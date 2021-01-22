# pylint: disable=unsubscriptable-object, global-statement
from pprint import pprint
from time import time

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .db import DATABASE_URI, db_conn, create_engine
from .logs import get_logger
from .resources import messages_router

logger = get_logger(__name__)


app = FastAPI(
    title="Hermes Messaging API",
    description="Luiza Labs Code Challenge",
    docs_url=None,
    redoc_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages_router)


# Database event, setting session dependency
# Global is anti pattern nowadays, but works well in dealing with async connection pool
@app.on_event("startup")
def open_database_connection_pools():
    global db_conn
    db_conn = create_engine(DATABASE_URI)


@app.on_event("shutdown")
def close_database_connection_pools():
    global db_conn
    if db_conn:
        db_conn.dispose()


# Middlewares
@app.middleware("http")
async def log_request_and_response_and_timeit(request: Request, call_next) -> Response:
    logger.info("Request -> %s", pprint(request.__dict__))
    start_time = time()

    response = await call_next(request)

    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    logger.info("Response -> %s", pprint(response.__dict__))
    logger.info("Executed in %s", process_time)

    return response


# Dummy healthcheck endpoint
@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"health": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
